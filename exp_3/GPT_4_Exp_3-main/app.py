
from flask import Flask, render_template, request, jsonify
import pandas as pd
import requests
import os

app = Flask(__name__)

CSV_FILE = os.path.join("data", "emails.csv")
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"


def ask_ollama(prompt):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=180
    )
    response.raise_for_status()
    return response.json()["response"].strip()


def get_records():
    try:
        df = pd.read_csv(CSV_FILE).fillna("")
        return df.to_dict(orient="records")
    except (FileNotFoundError, pd.errors.EmptyDataError):
        return []


@app.route("/")
def home():
    records = get_records()
    return render_template("index.html", records=records)


@app.route("/process", methods=["POST"])
def process_email():
    data = request.get_json(silent=True) or {}

    name = data.get("name", "").strip()
    subject = data.get("subject", "").strip()
    email = data.get("email", "").strip()
    tone = data.get("tone", "Professional").strip()

    if not name or not subject or not email:
        return jsonify({
            "error": "Please enter the customer name, subject, and email."
        }), 400

    try:
        # 1. Detect intent
        intent = ask_ollama(
            "Classify this customer email into one category: "
            "Delivery Issue, Refund Request, Product Complaint, "
            "Technical Support, Order Cancellation, General Inquiry.\n"
            f"Subject: {subject}\nEmail: {email}\n"
            "Return only the category name."
        )

        # 2. Find a similar email record
        records = get_records()
        previous_email = ""
        previous_reply = ""

        if records:
            from difflib import SequenceMatcher

            best_score = -1
            for record in records:
                old_email = str(record.get("Customer_Email", ""))
                score = SequenceMatcher(
                    None, email.lower(), old_email.lower()
                ).ratio()

                if score > best_score:
                    best_score = score
                    previous_email = old_email
                    previous_reply = str(
                        record.get("Previous_Reply", "")
                    )

        # 3. Generate a customer reply
        reply = ask_ollama(
            "You are a helpful customer support assistant. "
            "Write a clear, polite email reply to the customer. "
            "Do not invent order status, refunds, or actions already taken. "
            "Use the previous reply only as a reference.\n"
            f"Customer name: {name}\n"
            f"Subject: {subject}\n"
            f"Customer email: {email}\n"
            f"Detected intent: {intent}\n"
            f"Similar previous email: {previous_email}\n"
            f"Previous reply: {previous_reply}\n"
            "Write only the email reply."
        )

        # 4. Adjust reply to selected tone
        final_reply = ask_ollama(
            f"Rewrite this customer support email in a {tone} tone. "
            "Keep the meaning accurate and do not invent facts.\n"
            f"Email reply:\n{reply}"
        )

        # 5. Summarize the customer's email
        summary = ask_ollama(
            "Summarize this customer email in no more than 50 words.\n"
            f"Subject: {subject}\nEmail: {email}"
        )

        # 6. Save the generated result
        os.makedirs("outputs", exist_ok=True)
        with open(
            "outputs/generated_reply.txt",
            "a",
            encoding="utf-8"
        ) as file:
            file.write(
                f"\n{'=' * 50}\n"
                f"Customer: {name}\n"
                f"Subject: {subject}\n"
                f"Intent: {intent}\n"
                f"Tone: {tone}\n"
                f"Customer Email: {email}\n"
                f"Generated Reply:\n{final_reply}\n"
                f"Summary: {summary}\n"
            )

        return jsonify({
            "intent": intent,
            "reply": final_reply,
            "summary": summary,
            "similar_email": previous_email or "No previous record found"
        })

    except requests.RequestException:
        return jsonify({
            "error": "Cannot connect to Ollama. Make sure Ollama is running and llama3.2 is installed."
        }), 503
    except Exception as error:
        app.logger.exception("Email processing failed")
        return jsonify({
            "error": f"Processing failed: {error}"
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
