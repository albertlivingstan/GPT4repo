# Experiment 2: AI Blog Content Generator

An interactive, AI-driven blog generation application developed using **Flask** and local LLM execution with **Ollama (`llama3.2`)**.

---

## 📌 Overview

The **AI Blog Content Generator** enables content creators, marketers, and students to quickly draft structured, high-quality blog posts. By prompting local language models, the system produces coherent articles customized by topic, audience, tone, style, and word count.

### Key Capabilities
- **Structured Output Generation**: Produces blog posts formatted with an engaging title, introduction, substantive body sections, and a concise conclusion.
- **Tone & Audience Adaptation**: Adapts vocabulary and voice based on user requests (e.g., beginner-friendly, technical, persuasive, conversational).
- **Privacy & Local Execution**: Runs locally using Ollama (`llama3.2`), ensuring zero external API cost and full data confidentiality.
- **Web UI & REST API**: Features a clean, responsive web interface communicating with Flask JSON endpoints.

---

## 📁 Project Structure

```text
exp_2/GPT_4_Exp_2-main/
├── app.py                # Main Flask application and Ollama inference logic
├── templates/
│   └── index.html        # Web interface front-end
├── static/
│   ├── script.js         # Client-side asynchronous interaction handling
│   └── style.css         # Modern user interface styling
└── README.md             # Documentation
```

---

## 🛠️ Prerequisites

1. **Python 3.10+**
2. **Ollama**: [Download & install Ollama](https://ollama.com/)
3. **Llama 3.2 Model**:
   ```bash
   ollama pull llama3.2
   ```

---

## 🚀 Installation & Setup

1. **Navigate to the experiment directory**:
   ```bash
   cd exp_2/GPT_4_Exp_2-main
   ```

2. **Create and activate a virtual environment**:
   ```bash
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate

   # Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install flask ollama
   ```

4. **Ensure Ollama service is running**:
   ```bash
   ollama serve
   ```

5. **Start the Flask application**:
   ```bash
   python app.py
   ```

6. **Access the application**:
   Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your web browser.

---

## 💡 Example Prompts to Try

- *"Write a beginner-friendly 500-word blog post on the basics of Quantum Computing."*
- *"Create an engaging lifestyle blog about morning routines for peak productivity."*
- *"Draft a technical overview explaining the difference between REST and GraphQL for junior developers."*

---

## ⚙️ Architecture & Technical Flow

```text
[ User Prompt via Browser ]
            │
            ▼
   [ POST /chat (Flask) ]
            │
            ▼
[ System Prompt & Context Formatting ]
            │
            ▼
 [ Ollama API (llama3.2) ]
            │
            ▼
   [ JSON Response ] ──> [ Browser Dynamic Render ]
```

