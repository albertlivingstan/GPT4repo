# 24CS2506 – Building Applications Using GPT-4 & LLMs

A comprehensive repository containing six end-to-end applied AI laboratory projects and intelligent systems developed for **Building Applications using GPT-4 / Large Language Models**.

This repository spans diverse real-world domains—including e-commerce RAG chatbots, automated content generation, customer support email workflow automation, explainable recommender engines, legal contract audits, and healthcare symptom triage.

---

## 📑 Table of Contents

- [Repository Architecture](#-repository-architecture)
- [Comparative Analysis of All Experiments](#-comparative-analysis-of-all-experiments)
- [Detailed Experiment Breakdown](#-detailed-experiment-breakdown)
  - [Experiment 1: ECommerceGPT — AI-Powered E-Commerce Chatbot](#experiment-1-ecommercegpt--ai-powered-e-commerce-chatbot)
  - [Experiment 2: AI Blog Content Generator](#experiment-2-ai-blog-content-generator)
  - [Experiment 3: Intelligent Customer Email Assistant](#experiment-3-intelligent-customer-email-assistant)
  - [Experiment 4: Personalized Recommendation & Explanation System](#experiment-4-personalized-recommendation--explanation-system)
  - [Experiment 5: Automated Legal Document Analyzer](#experiment-5-automated-legal-document-analyzer)
  - [Experiment 6: AI Clinical Decision Support & Symptom Checker](#experiment-6-ai-clinical-decision-support--symptom-checker)
- [Prerequisites & Environment Setup](#-prerequisites--environment-setup)
- [How to Run Each Experiment](#-how-to-run-each-experiment)
- [Design Patterns & Engineering Best Practices](#-design-patterns--engineering-best-practices)

---

## 🏛️ Repository Architecture

```text
gpt4repo/
├── README.md                      # Root repository documentation (this file)
├── exp_1/                         # Experiment 1: E-Commerce RAG Chatbot
│   └── GPT-main/
│       ├── app.py                 # Flask web server & chat endpoints
│       ├── chatbot.py             # Orchestrator & fallback response handler
│       ├── create_embeddings.py   # Embedding & TF-IDF indexing script
│       ├── requirements.txt       # Dependencies (Flask, pandas, scikit-learn, etc.)
│       ├── modules/               # Modular RAG & classification engines
│       ├── data/                  # FAQ, products, and customer review datasets
│       ├── templates/ & static/   # Web chat user interface
│       └── README.md
├── exp_2/                         # Experiment 2: AI Blog Generator
│   └── GPT_4_Exp_2-main/
│       ├── app.py                 # Flask application connected to Ollama
│       ├── templates/ & static/   # Interactive web prompt interface
│       └── README.md
├── exp_3/                         # Experiment 3: Intelligent Email Assistant
│   └── GPT_4_Exp_3-main/
│       ├── app.py                 # Flask web interface
│       ├── main.py                # Interactive CLI mode
│       ├── *_module.py            # Intent, retrieval, reply, tone, summary modules
│       ├── data/emails.csv        # Historical email precedents
│       ├── outputs/               # Saved generated replies & summaries
│       └── README.md
├── exp_4/                         # Experiment 4: Explainable Recommendation Engine
│   └── GPT_4_Exp_4-main/
│       ├── app.py                 # Web application
│       ├── main.py                # Terminal interactive mode
│       ├── *_module.py            # Profile, prompt, ranking, explanation, feedback
│       ├── recommendations.txt    # Saved recommendation logs
│       └── README.md
├── exp_5/                         # Experiment 5: Legal Document Analyzer
│   └── GPT_4_Exp_5-main/
│       ├── app.py                 # Streamlit web app & contract audit pipeline
│       ├── requirements.txt       # Streamlit, PyPDF, Ollama
│       ├── outputs/               # Saved timestamped audit reports
│       └── README.md
└── exp_6/                         # Experiment 6: Medical Decision Support Assistant
    └── GPT_4_Exp_6-main/
        ├── app.py                 # Flask web application
        ├── main.py                # Interactive terminal driver
        ├── *_module.py            # Intake, symptom extraction, safety, analysis
        ├── requirements.txt       # OpenAI, Flask, Pandas
        ├── data/sample_cases.csv  # Benchmark patient scenarios
        ├── outputs/               # Saved clinical summary reports
        └── README.md
```

---

## 📊 Comparative Analysis of All Experiments

| # | Experiment Name | Domain | Core AI / ML Capabilities | Model(s) Used | User Interface |
|---|---|---|---|---|---|
| **1** | **ECommerceGPT** | E-Commerce Retail | RAG, TF-IDF Cosine Similarity, FAQ Matching, Sentiment Analysis | Qwen 2.5:3b / Llama 3.2 via Ollama | Responsive Web Chat UI |
| **2** | **AI Blog Content Generator** | Content Generation | Prompt engineering, long-form structured drafting, tone/audience conditioning | Llama 3.2 via Ollama | Web UI (Flask) |
| **3** | **Intelligent Email Assistant** | Customer Support | Intent classification, few-shot historical retrieval, tone adaptation, summarization | Llama 3.2 via Ollama | Dual: Web UI + Interactive CLI |
| **4** | **Personalized Recommendation System** | Education / EdTech | Constrained JSON generation, multi-criteria ranking, explainable AI (XAI), human-in-the-loop feedback | Llama 3.2 via Ollama (`format="json"`) | Dual: Web UI + Interactive CLI |
| **5** | **Automated Legal Document Analyzer** | Legal Tech / Contracts | PDF/TXT extraction, 11-point contract clause parsing, risk identification, contract Q&A | Llama 3.2:3b via Ollama | Streamlit Interactive Dashboard |
| **6** | **AI Medical Symptom Checker** | Healthcare / Clinical Decision Support | Symptom parsing, red flag triage, anamnesis follow-up question generation, guarded diagnostic prompts | GPT-4 / Safe Clinical Fallback | Dual: Web UI + Interactive CLI |

---

## 🔍 Detailed Experiment Breakdown

### Experiment 1: ECommerceGPT — AI-Powered E-Commerce Chatbot
- **Objective**: Develop an enterprise-ready retail assistant capable of handling pre-sales, product discovery, order support, and review summarization.
- **Key Modules**:
  - `intent_module.py`: Detects whether user wants FAQs, product recommendations, item specs, or review insights.
  - `faq_module.py`: Performs TF-IDF cosine similarity search across `data/faq.csv`. If confidence exceeds threshold, provides instant answer.
  - `recommendation_module.py`: Matches buyer specifications with items in `data/products.csv`.
  - `product_module.py`: Answers granular product inquiries with strict context grounding.
  - `review_module.py`: Analyzes sentiment in `data/reviews.csv` and compiles pros/cons.
- **Fail-Safe Mechanism**: Includes local rule-based deterministic fallback responses if the Ollama daemon is unreachable.

### Experiment 2: AI Blog Content Generator
- **Objective**: Streamline the creation of search-optimized, structured blog articles.
- **Key Features**:
  - Automatically structures output with engaging title, introduction hook, bulleted/subheaded main body, and takeaway conclusion.
  - Dynamically injects style, target audience persona, and length constraints into the model system prompt.
  - Minimalist, fast, asynchronous web application.

### Experiment 3: Intelligent Customer Email Assistant
- **Objective**: Automate Tier-1 customer support triage, draft generation, and ticketing summaries.
- **Workflow**:
  1. Classifies email intent into 6 major operational categories.
  2. Retrieves historical resolution precedents from `data/emails.csv`.
  3. Composes an initial resolution draft combining context and LLM fluency.
  4. Modifies tone between *Friendly*, *Formal/Professional*, or *Empathetic*.
  5. Produces an executive summary and appends records to `outputs/generated_reply.txt`.

### Experiment 4: Personalized Recommendation & Explanation System
- **Objective**: Deliver explainable recommendations with verified JSON structure and dynamic user feedback loops.
- **Highlights**:
  - **JSON Mode**: Leverages Ollama's schema-enforced output to guarantee consistent response parsing.
  - **Explainability**: Every recommended item includes a score (0–100%) and a human-understandable justification.
  - **Interactive Refinement**: Allows users to provide feedback, triggering prompt-level re-ranking.

### Experiment 5: Automated Legal Document Analyzer
- **Objective**: Accelerate contract compliance review for non-disclosure agreements, service contracts, and vendor terms.
- **Key Highlights**:
  - Powered by a responsive **Streamlit** dashboard.
  - Handles multi-page `.pdf` and `.txt` uploads via `pypdf`.
  - Evaluates 11 critical contractual vectors: parties, consideration, term, breach conditions, liabilities, and potential ambiguities.
  - Generates downloadable, timestamped review reports in `outputs/`.

### Experiment 6: AI Clinical Decision Support & Symptom Checker
- **Objective**: Provide structured health consultation assistance while enforcing strict patient safety safeguards.
- **Safety & Guardrails**:
  - Non-diagnostic design: Emphasizes informational guidance rather than authoritative diagnosis.
  - Red-flag detection for immediate emergency room referral (e.g., chest pain, respiratory distress).
  - Identifies missing clinical context (onset, pain severity, preexisting conditions) and asks clarifying follow-up questions.
  - Compatible with OpenAI `gpt-4` with local fallback support.

---

## 🛠️ Prerequisites & Environment Setup

### 1. System Requirements
- macOS, Linux, or Windows 10/11
- Python 3.10 or higher
- [Ollama](https://ollama.com/) (for running local open-weights models)

### 2. Local LLM Setup
Pull the models used across the experiments:
```bash
# Pull Llama 3.2 (used by Exp 2, 3, 4, 5)
ollama pull llama3.2

# Pull Qwen 2.5 (used by Exp 1)
ollama pull qwen2.5:3b

# Start the Ollama background daemon
ollama serve
```

---

## 🚀 How to Run Each Experiment

### Running Experiment 1 (ECommerceGPT)
```bash
cd exp_1/GPT-main
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python app.py
# Access at http://127.0.0.1:5000
```

### Running Experiment 2 (AI Blog Generator)
```bash
cd exp_2/GPT_4_Exp_2-main
python3 -m venv venv && source venv/bin/activate
pip install flask ollama
python app.py
# Access at http://127.0.0.1:5000
```

### Running Experiment 3 (Intelligent Customer Email Assistant)
```bash
cd exp_3/GPT_4_Exp_3-main
python3 -m venv venv && source venv/bin/activate
pip install flask pandas requests
# Web interface:
python app.py
# Or CLI interactive mode:
python main.py
```

### Running Experiment 4 (Personalized Recommendation System)
```bash
cd exp_4/GPT_4_Exp_4-main
python3 -m venv venv && source venv/bin/activate
pip install flask ollama
# Web interface:
python app.py
# Or CLI interactive mode:
python main.py
```

### Running Experiment 5 (Legal Document Analyzer)
```bash
cd exp_5/GPT_4_Exp_5-main
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
# Access at http://localhost:8501
```

### Running Experiment 6 (Medical Decision Support Assistant)
```bash
cd exp_6/GPT_4_Exp_6-main
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt flask pandas
# (Optional) Export your OpenAI API Key if using GPT-4:
# export OPENAI_API_KEY="sk-..."
# Web interface:
python app.py
# Or CLI interactive mode:
python main.py
```

---

## 💡 Design Patterns & Engineering Best Practices

1. **Modular Architecture**: Every experiment isolates input intake, prompt construction, model inference, safety validation, and persistence into dedicated modules.
2. **Local-First Privacy**: By utilizing Ollama with models like `llama3.2` and `qwen2.5`, all user interactions, customer emails, and legal documents remain entirely on the local machine.
3. **Graceful Degradation**: Core applications (such as Exp 1 and Exp 6) include fallback responses so that applications continue functioning smoothly even during network outages or API quota limits.
4. **Structured Generation**: Heavy reliance on constrained prompting and JSON format enforcement avoids hallucinated formats and ensures consistent serialization.

