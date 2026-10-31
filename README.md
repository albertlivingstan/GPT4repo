# 24CS2506 – Building Applications Using GPT-4 & LLMs

A comprehensive repository containing six end-to-end applied AI laboratory projects and intelligent systems developed for **Building Applications using GPT-4 / Large Language Models**.

This repository spans diverse real-world domains—including e-commerce RAG chatbots, automated content generation, customer support email workflow automation, explainable recommender engines, legal contract audits, and healthcare symptom triage.

---

## ⚡ Quickstart: Run All 6 Websites With ONE Command

You can launch all 6 experiments concurrently on dedicated ports with a single command from the project root:

```bash
./start.sh
```

*(or equivalently using Python)*:

```bash
python3 run_all.py
```

### 🌐 Live Port & URL Mapping

Once running, open any link below in your browser:

| # | Experiment Name | Port | Live Browser URL | Description |
|---|---|---|---|---|
| **1** | **ECommerceGPT** | `5001` | [http://127.0.0.1:5001](http://127.0.0.1:5001) | RAG-powered retail chatbot with TF-IDF search, FAQs & sentiment |
| **2** | **BlogStudio Pro** | `5002` | [http://127.0.0.1:5002](http://127.0.0.1:5002) | Advanced writing studio with real-time Flesch readability, SEO & inline AI polish |
| **3** | **MailSense AI** | `5003` | [http://127.0.0.1:5003](http://127.0.0.1:5003) | Support ticket triage, 1-click test scenarios, tone rewriting & precedent search |
| **4** | **PathFinder AI** | `5004` | [http://127.0.0.1:5004](http://127.0.0.1:5004) | Explainable learning recommender with match scoring & feedback refinement |
| **5** | **LexiGuard AI** | `8501` | [http://localhost:8501](http://localhost:8501) | Streamlit legal audit dashboard with sample contracts, clause checks & contract Q&A |
| **6** | **MediAssist AI** | `5006` | [http://127.0.0.1:5006](http://127.0.0.1:5006) | Clinical decision support, quick-add symptoms, red-flag triage & print-ready reports |

> Press <kbd>Ctrl</kbd> + <kbd>C</kbd> in your terminal to cleanly stop all 6 background servers simultaneously.

---

## 📑 Table of Contents

- [Quickstart: Run All 6 Websites With ONE Command](#-quickstart-run-all-6-websites-with-one-command)
- [Repository Architecture](#-repository-architecture)
- [Comparative Analysis of All Experiments](#-comparative-analysis-of-all-experiments)
- [Detailed Experiment Breakdown](#-detailed-experiment-breakdown)
  - [Experiment 1: ECommerceGPT — AI-Powered E-Commerce Chatbot](#experiment-1-ecommercegpt--ai-powered-e-commerce-chatbot)
  - [Experiment 2: BlogStudio Pro — AI Content Workspace](#experiment-2-blogstudio-pro--ai-content-workspace)
  - [Experiment 3: MailSense AI — Intelligent Customer Support Co-Pilot](#experiment-3-mailsense-ai--intelligent-customer-support-co-pilot)
  - [Experiment 4: PathFinder AI — Explainable Recommendation System](#experiment-4-pathfinder-ai--explainable-recommendation-system)
  - [Experiment 5: LexiGuard AI — Automated Legal Contract & Risk Analyzer](#experiment-5-lexiguard-ai--automated-legal-contract--risk-analyzer)
  - [Experiment 6: MediAssist AI — Clinical Decision Support Assistant](#experiment-6-mediassist-ai--clinical-decision-support-assistant)
- [Prerequisites & Environment Setup](#-prerequisites--environment-setup)
- [How to Run Experiments Individually](#-how-to-run-experiments-individually)
- [Design Patterns & Engineering Best Practices](#-design-patterns--engineering-best-practices)

---

## 🏛️ Repository Architecture

```text
gpt4repo/
├── start.sh                       # One-command executable bash runner
├── run_all.py                     # Supervisor Python process managing all 6 servers
├── README.md                      # Root repository documentation (this file)
├── .gitignore                     # Clean repository ignore specification
├── exp_1/                         # Experiment 1: E-Commerce RAG Retail Chatbot
│   └── GPT-main/
│       ├── app.py                 # Flask web server (Port 5001)
│       ├── chatbot.py             # Orchestrator & fallback response handler
│       ├── create_embeddings.py   # Embedding & TF-IDF indexing script
│       ├── modules/               # Modular RAG & classification engines
│       ├── data/                  # FAQ, products, and customer review datasets
│       └── README.md
├── exp_2/                         # Experiment 2: BlogStudio Pro
│   └── GPT_4_Exp_2-main/
│       ├── app.py                 # Flask server (Port 5002) with readability analytics
│       ├── templates/ & static/   # Modern 2-column studio with live preview & inline AI
│       └── README.md
├── exp_3/                         # Experiment 3: MailSense AI
│   └── GPT_4_Exp_3-main/
│       ├── app.py                 # Flask server (Port 5003)
│       ├── data/emails.csv        # Precedent customer interactions
│       ├── templates/ & static/   # Modern support triage desk UI
│       └── README.md
├── exp_4/                         # Experiment 4: PathFinder AI
│   └── GPT_4_Exp_4-main/
│       ├── app.py                 # Flask server (Port 5004)
│       ├── *_module.py            # Profile, recommendation, ranking, and feedback modules
│       ├── templates/ & static/   # Explainable curriculum recommender with feedback loop
│       └── README.md
├── exp_5/                         # Experiment 5: LexiGuard AI
│   └── GPT_4_Exp_5-main/
│       ├── app.py                 # Streamlit dashboard (Port 8501) with sample NDAs & Q&A
│       └── README.md
└── exp_6/                         # Experiment 6: MediAssist AI
    └── GPT_4_Exp_6-main/
        ├── app.py                 # Flask server (Port 5006)
        ├── *_module.py            # Intake, symptom extraction, safety & differential analysis
        ├── templates/ & static/   # Clinical triage UI with quick-add symptom tags
        └── README.md
```

---

## 📊 Comparative Analysis of All Experiments

| # | Experiment Name | Domain | Core AI / ML Capabilities | Model(s) Used | User Interface | Port |
|---|---|---|---|---|---|---|
| **1** | **ECommerceGPT** | E-Commerce Retail | RAG, TF-IDF Cosine Similarity, FAQ Matching, Sentiment Analysis | Qwen 2.5:3b / Llama 3.2 via Ollama | Responsive Web Chat UI | `5001` |
| **2** | **BlogStudio Pro** | Content Generation | Structured prompt engineering, live Flesch readability, inline AI rewriter, SEO checks | Llama 3.2 via Ollama | Two-Column Studio UI | `5002` |
| **3** | **MailSense AI** | Customer Support | Intent classification, few-shot historical retrieval, tone adaptation, summarization | Llama 3.2 via Ollama | Support Desk Co-Pilot | `5003` |
| **4** | **PathFinder AI** | EdTech / Careers | Constrained JSON generation, match scoring (0-100%), XAI justifications, interactive feedback | Llama 3.2 via Ollama (`format="json"`) | Learning Pathway Studio | `5004` |
| **5** | **LexiGuard AI** | Legal Tech / Contracts | PDF/TXT extraction, 11-point contract clause parsing, risk assessment, contract Q&A | Llama 3.2:3b via Ollama | Streamlit Dashboard | `8501` |
| **6** | **MediAssist AI** | Healthcare & Triage | Symptom parsing, red-flag emergency triage, clinical follow-up questions, non-diagnostic safety | Llama 3.2 / GPT-4 / Safe Fallback | Clinical Triage Portal | `5006` |

---

## 🔍 Detailed Experiment Breakdown

### Experiment 1: ECommerceGPT — AI-Powered E-Commerce Chatbot
- **Objective**: Develop an enterprise-ready retail assistant capable of handling pre-sales, product discovery, order support, and review summarization.
- **Key Modules**:
  - `intent_module.py`: Detects intent (FAQ, recommendations, specs, review sentiment).
  - `faq_module.py`: Cosine similarity search over `data/faq.csv` with confidence thresholding.
  - `recommendation_module.py`: Matches buyer specifications with items in `data/products.csv`.
  - `product_module.py` & `review_module.py`: Grounded product specs and sentiment breakdown.

### Experiment 2: BlogStudio Pro — AI Content Workspace
- **Objective**: Full-featured content creation workspace with architectural planning and real-time linguistic metrics.
- **Key Features**:
  - Computes real-time word count, reading time, and **Flesch Reading Ease** readability scores.
  - **Inline AI Rewriting**: One-click actions to *Expand*, *Make Concise*, *Simplify Language*, and *Executive Tone*.
  - **AI Ideation & Brainstormer**: Generates viral titles, H2/H3 outlines, SEO keyword maps, and introductory hooks.
  - Multi-format export: Markdown (`.md`), Plain Text (`.txt`), HTML (`.html`), or Print/PDF.

### Experiment 3: MailSense AI — Intelligent Customer Support Co-Pilot
- **Objective**: Automate Tier-1 customer support triage, draft generation, and ticketing summaries.
- **Key Features**:
  - Automatically classifies emails into 6 major operational categories (*Delivery Issue*, *Refund Request*, *Technical Support*, etc.).
  - Retrieves nearest historical precedents from `data/emails.csv`.
  - Adapts reply tone across *Empathetic*, *Professional*, *Friendly*, or *Concise*.
  - Includes 1-click test scenarios for instant demonstration.

### Experiment 4: PathFinder AI — Explainable Recommendation System
- **Objective**: Deliver explainable learning pathways with verified JSON schemas and human-in-the-loop adaptation.
- **Key Features**:
  - **XAI Reasoning**: Every recommendation includes a match percentage (e.g., `96% Match`), difficulty grade, and clear justification.
  - **Human-in-the-Loop Refinement**: Critique recommendations (e.g., *"Focus exclusively on free open-source GitHub projects"*) and observe live curriculum adaptation.
  - Built-in personas for *AI Systems Engineer*, *Data Analyst*, and *Cloud Architect*.

### Experiment 5: LexiGuard AI — Automated Legal Contract & Risk Analyzer
- **Objective**: Accelerate contract compliance review for non-disclosure agreements, service contracts, and vendor terms.
- **Key Features**:
  - Supports uploading `.pdf` or `.txt` agreements, or selecting built-in sample contracts (*Mutual NDA*, *SaaS MSA*).
  - Audits 11 critical vectors: parties, obligations, consideration, liabilities, duration, and potential risks.
  - **Interactive Contract Q&A**: Ask ad-hoc questions directly over the uploaded contract.

### Experiment 6: MediAssist AI — Clinical Decision Support Assistant
- **Objective**: Provide structured health consultation assistance while enforcing strict patient safety safeguards.
- **Key Features**:
  - Quick-add symptom chips (`+ Headache`, `+ Fever`, `+ Cough`, `+ Fatigue`, etc.).
  - Red-flag detection for immediate emergency room referral.
  - Formats patient vitals, differential considerations, and recommended next steps into a print-ready clinical report.

---

## 🛠️ Prerequisites & Environment Setup

### 1. System Requirements
- macOS, Linux, or Windows 10/11
- Python 3.10 or higher
- [Ollama](https://ollama.com/) (for running local open-weights models)

### 2. Local LLM Setup
Pull the models used across the experiments:
```bash
# Pull Llama 3.2
ollama pull llama3.2

# Pull Qwen 2.5
ollama pull qwen2.5:3b

# Start the Ollama background daemon
ollama serve
```

---

## 🚀 How to Run Experiments Individually

If you prefer to run an experiment by itself rather than using `./start.sh`:

```bash
# Experiment 1 (Port 5001)
cd exp_1/GPT-main && python3 app.py

# Experiment 2 (Port 5002)
cd exp_2/GPT_4_Exp_2-main && python3 app.py

# Experiment 3 (Port 5003)
cd exp_3/GPT_4_Exp_3-main && python3 app.py

# Experiment 4 (Port 5004)
cd exp_4/GPT_4_Exp_4-main && python3 app.py

# Experiment 5 (Port 8501)
cd exp_5/GPT_4_Exp_5-main && streamlit run app.py --server.port 8501

# Experiment 6 (Port 5006)
cd exp_6/GPT_4_Exp_6-main && python3 app.py
```
