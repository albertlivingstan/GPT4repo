# Experiment 2: BlogStudio Pro — Advanced AI Writing Workspace

An enterprise-grade, interactive AI content creation studio developed using **Flask** and local LLM execution with **Ollama (`llama3.2`, `qwen2.5`)**.

---

## 📌 Overview

**BlogStudio Pro** transforms the basic content generator into a full-featured SaaS-grade AI writing studio. It provides comprehensive blog architectural planning, real-time readability analytics, inline text polishing, and search engine optimization (SEO) tools powered entirely by local open-weights language models.

### 🌟 Advanced Features
- **Structured Content Architecture**: Generates publication-ready articles featuring high-CTR titles, executive key takeaways callout boxes, table of contents, and schema-ready FAQs.
- **Dynamic Model Selection**: Auto-detects local Ollama models (`llama3.2`, `qwen2.5:3b`, `gemma3:1b`) allowing on-the-fly model switching directly from the UI header.
- **Live Content Metrics & Readability**: Computes real-time word count, character count, sentence count, estimated reading time, and **Flesch Reading Ease** readability scores.
- **Three-Tier Studio View**:
  - 📄 **Rich Preview**: Formatted headings, styled blockquotes, code blocks, and bullet points.
  - 📝 **Raw Markdown Editor**: Live bidirectional markdown editor.
  - 📊 **SEO & Metrics**: Structural checklist (H1/H2 hierarchy, FAQ verification, optimal word count).
- **Inline AI Rewriter & Polisher**:
  - `Expand`: Adds depth, real-world examples, and data analogies.
  - `Make Concise`: Condenses verbose sections into high-impact copy.
  - `Simplify`: Rewrites complex explanations in plain English.
  - `Executive Tone`: Polishes language for enterprise and leadership audiences.
  - `Bulletize`: Transforms paragraphs into scannable key takeaways.
- **Integrated AI Ideator / Brainstormer**:
  - Viral title generator (5 high-converting angles).
  - Structural outline architect.
  - SEO keyword map with search intent.
  - Hook brainstormer (story hook, statistical hook, question hook).
- **Multi-Format Export & Draft History**:
  - Export to Markdown (`.md`), Plain Text (`.txt`), Web HTML (`.html`), or Print/PDF.
  - Automatic persistence to `outputs/` with historical draft reloader.

---

## 📁 Project Structure

```text
exp_2/GPT_4_Exp_2-main/
├── app.py                # Flask application, Ollama orchestrator & REST API
├── templates/
│   └── index.html        # Modern two-column studio UI with live preview & tabs
├── static/
│   ├── script.js         # Asynchronous client engine, markdown parser, export handlers
│   └── style.css         # Modern SaaS indigo/slate design system
├── outputs/              # Saved generated articles and JSON metadata
└── README.md             # Documentation
```

---

## 🛠️ API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Web studio interface |
| `GET` | `/api/models` | List locally installed Ollama models |
| `POST` | `/generate-blog` | Main article generator with structural constraints & stats |
| `POST` | `/api/stream` | Server-Sent Events (SSE) streaming output endpoint |
| `POST` | `/api/quick-assist` | AI Brainstormer (titles, outlines, keywords, hooks) |
| `POST` | `/api/refine` | Inline AI rewriting (expand, shorten, simplify, executive tone) |
| `GET` | `/api/history` | List previously saved articles and metadata |
| `GET` | `/api/article/<id>` | Retrieve a saved article by ID |

---

## 🚀 How to Run

1. **Ensure Ollama is running**:
   ```bash
   ollama serve
   ```

2. **Launch directly**:
   ```bash
   cd exp_2/GPT_4_Exp_2-main
   ../../.venv_shared/bin/python app.py
   ```
   Open **[http://127.0.0.1:5002](http://127.0.0.1:5002)** in your browser.
