import os
import re
import json
from datetime import datetime
from difflib import SequenceMatcher
from pathlib import Path
from flask import Flask, render_template, request, jsonify
import pandas as pd
import requests
import ollama

app = Flask(__name__)

CSV_FILE = Path(__file__).parent / "data" / "emails.csv"
OUTPUT_FILE = Path(__file__).parent / "outputs" / "generated_reply.txt"

DEFAULT_MODEL = "llama3.2"
FALLBACK_MODELS = ["llama3.2", "llama3.2:3b", "llama3.2:latest", "qwen2.5:3b"]


def get_available_models():
    try:
        models_data = ollama.list()
        models_list = models_data.get("models", []) if isinstance(models_data, dict) else getattr(models_data, "models", [])
        names = []
        for m in models_list:
            if isinstance(m, dict):
                names.append(m.get("name") or m.get("model"))
            else:
                names.append(getattr(m, "name", "") or getattr(m, "model", ""))
        return [n for n in names if n] or FALLBACK_MODELS
    except Exception:
        return FALLBACK_MODELS


def resolve_model(requested=None):
    available = get_available_models()
    if requested and (requested in available or f"{requested}:latest" in available):
        return requested
    for candidate in [DEFAULT_MODEL] + FALLBACK_MODELS:
        for av in available:
            if candidate == av or av.startswith(candidate):
                return av
    return DEFAULT_MODEL


def ask_ollama(prompt, model=None):
    model_name = resolve_model(model)
    try:
        response = ollama.chat(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": 0.3}
        )
        return response.get("message", {}).get("content", "").strip()
    except Exception as e:
        # Fallback to direct HTTP if client fails
        res = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model_name, "prompt": prompt, "stream": False},
            timeout=120
        )
        res.raise_for_status()
        return res.json()["response"].strip()


def get_records():
    try:
        if CSV_FILE.exists():
            df = pd.read_csv(CSV_FILE).fillna("")
            return df.to_dict(orient="records")
    except Exception as e:
        print("Error reading emails.csv:", e)
    return []


@app.route("/")
def home():
    records = get_records()
    return render_template("index.html", records=records)


@app.route("/api/models")
def api_models():
    return jsonify({
        "models": get_available_models(),
        "active": resolve_model()
    })


@app.route("/api/samples")
def api_samples():
    samples = [
        {
            "name": "Sarah Jenkins",
            "subject": "Delayed Package #ORD-98213",
            "email": "Hello support, my order #ORD-98213 was supposed to arrive last Tuesday. The tracking page has not updated in 4 days and I urgently need these items for an event tomorrow. Please advise on when it will arrive or provide a refund.",
            "tone": "Empathetic"
        },
        {
            "name": "Marcus Vance",
            "subject": "Incorrect Invoice / Duplicate Charge",
            "email": "Hi, I was charged twice for subscription invoice #INV-4412 on October 28th ($49.00 x 2). Can you please look into your billing ledger and reverse the duplicate charge immediately?",
            "tone": "Professional"
        },
        {
            "name": "Elena Rostova",
            "subject": "Application Error on Checkout Page",
            "email": "Every time I try to complete my checkout with a Mastercard, the webpage throws a 500 internal server error. I have cleared my cache and tried another browser with no luck. Can you help?",
            "tone": "Friendly"
        }
    ]
    return jsonify({"samples": samples})


@app.route("/process", methods=["POST"])
def process_email():
    data = request.get_json(silent=True) or {}

    name = data.get("name", "").strip()
    subject = data.get("subject", "").strip()
    email = data.get("email", "").strip()
    tone = data.get("tone", "Professional").strip()
    model = data.get("model")

    if not name or not subject or not email:
        return jsonify({
            "error": "Please enter the customer name, subject, and message."
        }), 400

    try:
        # 1. Detect Intent
        intent_prompt = f"""Classify this customer support email into exactly one category:
Delivery Issue, Refund Request, Product Complaint, Technical Support, Order Cancellation, General Inquiry.

Customer Subject: {subject}
Customer Email: {email}

Return ONLY the single category name, with no extra punctuation or commentary."""

        intent = ask_ollama(intent_prompt, model=model).strip()

        # 2. Similarity match from database
        records = get_records()
        previous_email = ""
        previous_reply = ""
        best_score = -1

        if records:
            for record in records:
                old_email = str(record.get("Customer_Email", "") or record.get("Email", ""))
                score = SequenceMatcher(None, email.lower(), old_email.lower()).ratio()
                if score > best_score:
                    best_score = score
                    previous_email = old_email
                    previous_reply = str(record.get("Previous_Reply", "") or record.get("Reply", ""))

        # 3. Unified Generation: Draft context-aware response & summary in requested tone
        ref_text = f"Historical Reference Resolution:\n{previous_reply}" if previous_reply else ""
        prompt = f"""You are MailSense AI, an expert customer service specialist.
Compose a polite, highly empathetic, and professional resolution reply to the customer, adhering strictly to the '{tone}' tone.

Customer Name: {name}
Subject: {subject}
Customer Inquiry: {email}
Detected Category: {intent}
{ref_text}

Rules:
- Address the customer by name.
- Be constructive, professional, and clear.
- Do not make up fake tracking numbers or claim money is already in their bank.
- Match the requested tone: {tone}.

Provide the response in the following format:
REPLY:
[Your complete customer email reply here]

SUMMARY:
[A concise 1-2 sentence executive briefing for internal ticketing notes]"""

        result_raw = ask_ollama(prompt, model=model)

        final_reply = ""
        summary = ""

        if "REPLY:" in result_raw and "SUMMARY:" in result_raw:
            parts = result_raw.split("SUMMARY:")
            final_reply = parts[0].replace("REPLY:", "").strip()
            summary = parts[1].strip()
        else:
            final_reply = result_raw
            summary = f"Customer inquiry from {name} regarding {subject} categorized under {intent}."

        # 4. Save to outputs
        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
            f.write(
                f"\n{'=' * 60}\n"
                f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"Customer: {name}\n"
                f"Subject: {subject}\n"
                f"Intent: {intent}\n"
                f"Tone: {tone}\n"
                f"Summary: {summary}\n\n"
                f"Generated Reply:\n{final_reply}\n"
            )

        return jsonify({
            "success": True,
            "intent": intent,
            "reply": final_reply,
            "summary": summary,
            "similar_email": previous_email or "No direct historical match (standard protocol applied)"
        })

    except requests.RequestException:
        return jsonify({
            "error": "Could not connect to Ollama. Ensure the Ollama background daemon is running (`ollama serve`)."
        }), 503
    except Exception as error:
        app.logger.exception("Email processing failed")
        return jsonify({"error": f"Processing error: {str(error)}"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5003))
    print(f"Starting Exp 3 on port {port}")
    app.run(debug=True, port=port)
