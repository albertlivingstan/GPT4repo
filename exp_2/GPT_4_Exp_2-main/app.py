import os
import re
import json
import time
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, request, jsonify, Response, stream_with_context
import ollama

app = Flask(__name__)

DEFAULT_MODEL = "llama3.2"
FALLBACK_MODELS = ["llama3.2", "llama3.2:3b", "llama3.2:latest", "qwen2.5:3b"]

OUTPUT_DIR = Path(__file__).parent / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def get_available_models():
    """Retrieve models available in the local Ollama instance."""
    try:
        models_data = ollama.list()
        # Handle dict or object response from ollama client
        models_list = models_data.get("models", []) if isinstance(models_data, dict) else getattr(models_data, "models", [])
        names = []
        for m in models_list:
            if isinstance(m, dict):
                names.append(m.get("name") or m.get("model"))
            else:
                names.append(getattr(m, "name", "") or getattr(m, "model", ""))
        names = [n for n in names if n]
        if names:
            return names
    except Exception as e:
        print("Could not list Ollama models:", e)
    return FALLBACK_MODELS


def resolve_model(requested_model=None):
    """Find the best available model, falling back gracefully."""
    available = get_available_models()
    if requested_model and (requested_model in available or f"{requested_model}:latest" in available):
        return requested_model
    for candidate in [DEFAULT_MODEL] + FALLBACK_MODELS:
        for av in available:
            if candidate == av or av.startswith(candidate):
                return av
    return DEFAULT_MODEL


def calculate_readability(text):
    """Calculate approximate Flesch Reading Ease score and statistics."""
    words = re.findall(r"\b\w+\b", text)
    word_count = len(words)
    if word_count == 0:
        return {"word_count": 0, "reading_time_min": 0, "flesch_score": 100, "grade": "Very Easy"}

    sentences = re.split(r"[.!?]+", text)
    sentence_count = max(1, len([s for s in sentences if s.strip()]))

    # Approximate syllable count
    syllable_count = 0
    for w in words:
        w_lower = w.lower()
        count = len(re.findall(r"[aeiouy]+", w_lower))
        if w_lower.endswith("e") and not w_lower.endswith("le") and count > 1:
            count -= 1
        syllable_count += max(1, count)

    asl = word_count / sentence_count
    asw = syllable_count / word_count
    flesch = 206.835 - (1.015 * asl) - (84.6 * asw)
    flesch = max(0, min(100, round(flesch, 1)))

    if flesch >= 90:
        grade = "Very Easy (5th Grade)"
    elif flesch >= 80:
        grade = "Easy (6th Grade)"
    elif flesch >= 70:
        grade = "Fairly Easy (7th Grade)"
    elif flesch >= 60:
        grade = "Standard (8th-9th Grade)"
    elif flesch >= 50:
        grade = "Fairly Difficult (High School)"
    elif flesch >= 30:
        grade = "Difficult (College)"
    else:
        grade = "Very Confusing (Graduate)"

    reading_time = max(1, round(word_count / 200))

    return {
        "word_count": word_count,
        "character_count": len(text),
        "sentence_count": sentence_count,
        "reading_time_min": reading_time,
        "flesch_score": flesch,
        "grade": grade
    }


def build_system_prompt(style, tone, audience, word_count, keywords, include_faq, include_takeaways, include_toc):
    return f"""You are BlogStudio Pro, an elite AI copywriter and SEO content strategist.
Your task is to write a comprehensive, publication-ready, deeply engaging blog article.

Specifications:
- Writing Style: {style}
- Emotional Tone: {tone}
- Target Audience: {audience}
- Target Length: ~{word_count} words
{f"- Required SEO Keywords to seamlessly integrate: {keywords}" if keywords else ""}

Formatting & Structural Requirements:
1. Title: Start with a powerful, high-CTR H1 title (prefixed with single '# ').
2. Subtitle: Add a compelling 1-sentence teaser immediately below the title.
{("3. Key Takeaways Callout: Include a '> **Key Takeaways**' blockquote with 3-4 bullet points highlighting essential insights." if include_takeaways else "")}
{("4. Table of Contents: Provide an organized markdown bullet list outlining sections." if include_toc else "")}
5. Body Architecture:
   - Use descriptive H2 ('## ') and H3 ('### ') subheadings for clear hierarchy.
   - Use short, scannable paragraphs (2-4 sentences).
   - Use bolding, bullet points, data analogies, and concrete real-world examples to explain concepts.
{("6. FAQ Section: End with a '## Frequently Asked Questions' section containing 3 practical Q&As with concise answers." if include_faq else "")}
7. Conclusion: Wrap up with an empowering '## Conclusion & Next Steps' with an actionable call-to-action (CTA).
8. Do not output meta-commentary (e.g., do not say 'Here is your blog post:'). Begin directly with the # Title."""


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/models", methods=["GET"])
def api_models():
    models = get_available_models()
    active = resolve_model()
    return jsonify({
        "models": models,
        "active": active
    })


@app.route("/generate-blog", methods=["POST"])
@app.route("/chat", methods=["POST"])
def generate_blog():
    try:
        data = request.get_json(silent=True) or {}

        # Support both form payload and legacy 'message'
        topic = data.get("topic") or data.get("message") or ""
        topic = topic.strip()
        if not topic:
            return jsonify({"error": "Please provide an article topic or prompt."}), 400

        style = data.get("style", "Professional")
        tone = data.get("tone", "Informative & Engaging")
        audience = data.get("audience", "General / Industry Professionals")
        word_count = data.get("wordCount") or data.get("word_count") or 750
        instructions = (data.get("instructions") or "").strip()
        keywords = (data.get("keywords") or "").strip()
        model_name = resolve_model(data.get("model"))

        include_faq = bool(data.get("include_faq", True))
        include_takeaways = bool(data.get("include_takeaways", True))
        include_toc = bool(data.get("include_toc", False))

        system_prompt = build_system_prompt(
            style, tone, audience, word_count, keywords,
            include_faq, include_takeaways, include_toc
        )

        user_content = f"Write a complete article about:\n\nTOPIC: {topic}"
        if instructions:
            user_content += f"\n\nADDITIONAL USER INSTRUCTIONS:\n{instructions}"

        start_time = time.time()

        response = ollama.chat(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            options={"temperature": 0.7}
        )

        elapsed = round(time.time() - start_time, 2)
        blog_content = response.get("message", {}).get("content", "").strip()

        # Compute readability & metrics
        stats = calculate_readability(blog_content)
        stats["generation_time_sec"] = elapsed
        stats["model"] = model_name

        # Auto-save to outputs
        article_id = f"article_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        save_file = OUTPUT_DIR / f"{article_id}.md"
        meta_file = OUTPUT_DIR / f"{article_id}.json"

        save_file.write_text(blog_content, encoding="utf-8")
        meta_file.write_text(json.dumps({
            "id": article_id,
            "topic": topic,
            "created_at": datetime.now().isoformat(),
            "stats": stats,
            "params": {
                "style": style,
                "tone": tone,
                "audience": audience,
                "word_count": word_count,
                "keywords": keywords,
                "model": model_name
            }
        }, indent=2), encoding="utf-8")

        return jsonify({
            "success": True,
            "blog": blog_content,
            "content": blog_content,
            "response": blog_content,
            "stats": stats,
            "article_id": article_id
        })

    except Exception as e:
        app.logger.exception("Blog generation error")
        return jsonify({
            "error": f"Generation failed: {str(e)}. Ensure Ollama is running (`ollama serve`)."
        }), 500


@app.route("/api/stream", methods=["POST"])
def api_stream():
    """Server-Sent Events endpoint for real-time streaming generation."""
    data = request.get_json(silent=True) or {}
    topic = (data.get("topic") or data.get("message") or "").strip()
    if not topic:
        return jsonify({"error": "Topic required"}), 400

    style = data.get("style", "Professional")
    tone = data.get("tone", "Informative & Engaging")
    audience = data.get("audience", "Professionals")
    word_count = data.get("wordCount", 750)
    instructions = (data.get("instructions") or "").strip()
    keywords = (data.get("keywords") or "").strip()
    model_name = resolve_model(data.get("model"))

    system_prompt = build_system_prompt(
        style, tone, audience, word_count, keywords,
        include_faq=bool(data.get("include_faq", True)),
        include_takeaways=bool(data.get("include_takeaways", True)),
        include_toc=bool(data.get("include_toc", False))
    )

    user_content = f"Write a complete article about:\n\nTOPIC: {topic}"
    if instructions:
        user_content += f"\n\nADDITIONAL INSTRUCTIONS:\n{instructions}"

    def generate():
        try:
            stream = ollama.chat(
                model=model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content}
                ],
                stream=True,
                options={"temperature": 0.7}
            )
            for chunk in stream:
                token = chunk.get("message", {}).get("content", "")
                if token:
                    yield f"data: {json.dumps({'token': token})}\n\n"
            yield f"data: {json.dumps({'done': True})}\n\n"
        except Exception as err:
            yield f"data: {json.dumps({'error': str(err)})}\n\n"

    return Response(stream_with_context(generate()), mimetype="text/event-stream")


@app.route("/api/quick-assist", methods=["POST"])
def api_quick_assist():
    """Quick AI ideation: topic generator, catchy hooks, outline, SEO keywords."""
    data = request.get_json(silent=True) or {}
    prompt_type = data.get("type", "custom")
    user_input = (data.get("input") or "").strip()
    model_name = resolve_model(data.get("model"))

    if prompt_type == "topics":
        prompt = f"Suggest 5 viral, engaging blog post titles and brief angles for the subject: '{user_input}'. Format as a numbered list with a 1-sentence hook for each."
    elif prompt_type == "outline":
        prompt = f"Create a comprehensive, structured blog post outline with H2 and H3 sections for the topic: '{user_input}'. Include key points to cover in each section."
    elif prompt_type == "keywords":
        prompt = f"Provide 10 high-value primary and secondary SEO keywords for a blog about '{user_input}', including search intent (Informational/Commercial) and estimated ranking difficulty."
    elif prompt_type == "intro":
        prompt = f"Write 3 different high-converting introductory hooks (e.g. Statistical Hook, Story Hook, Provocative Question Hook) for an article on: '{user_input}'."
    else:
        prompt = user_input

    try:
        response = ollama.chat(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a master content strategist. Be direct, clear, and actionable. Do not use conversational filler."},
                {"role": "user", "content": prompt}
            ],
            options={"temperature": 0.7}
        )
        return jsonify({
            "success": True,
            "response": response.get("message", {}).get("content", "").strip()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/refine", methods=["POST"])
def api_refine():
    """Inline AI rewriting tools: simplify, expand, shorten, polish tone."""
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    action = data.get("action", "improve")
    model_name = resolve_model(data.get("model"))

    if not text:
        return jsonify({"error": "No text provided"}), 400

    action_instructions = {
        "expand": "Expand this text with rich real-world examples, deeper explanations, and supporting arguments without unnecessary fluff.",
        "shorten": "Condense this text to make it concise, crisp, and high-impact while preserving all key information.",
        "simplify": "Explain this text in plain, easy-to-understand English so a beginner can grasp it instantly.",
        "professional": "Rewrite this text in an authoritative, executive, and polished professional tone.",
        "casual": "Rewrite this text in a friendly, conversational, warm, and approachable tone.",
        "bullet_points": "Transform this paragraph into a scannable bullet-point summary."
    }

    instruction = action_instructions.get(action, "Improve clarity, flow, and impact.")

    try:
        response = ollama.chat(
            model=model_name,
            messages=[
                {"role": "system", "content": f"You are an expert copy editor. {instruction} Return ONLY the revised text with zero preamble or meta-chatter."},
                {"role": "user", "content": text}
            ]
        )
        revised = response.get("message", {}).get("content", "").strip()
        return jsonify({
            "success": True,
            "revised": revised
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/history", methods=["GET"])
def api_history():
    """Retrieve list of previously generated articles."""
    articles = []
    for meta_file in sorted(OUTPUT_DIR.glob("*.json"), reverse=True)[:20]:
        try:
            data = json.loads(meta_file.read_text(encoding="utf-8"))
            articles.append(data)
        except Exception:
            pass
    return jsonify({"articles": articles})


@app.route("/api/article/<article_id>", methods=["GET"])
def api_get_article(article_id):
    md_file = OUTPUT_DIR / f"{article_id}.md"
    meta_file = OUTPUT_DIR / f"{article_id}.json"
    if not md_file.exists():
        return jsonify({"error": "Article not found"}), 404

    content = md_file.read_text(encoding="utf-8")
    meta = json.loads(meta_file.read_text(encoding="utf-8")) if meta_file.exists() else {}
    return jsonify({
        "id": article_id,
        "content": content,
        "meta": meta
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5002))
    print("=" * 60)
    print("   BLOGSTUDIO PRO — ADVANCED AI WRITING WORKSPACE")
    print("=" * 60)
    print(f"Starting server on http://127.0.0.1:{port}")
    print("=" * 60)
    app.run(debug=True, port=port)
