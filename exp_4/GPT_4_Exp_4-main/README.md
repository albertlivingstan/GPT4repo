# Experiment 4: Personalized Recommendation & Explanation System

A modular recommendation engine that analyzes learner/user profiles, queries local LLMs with structured JSON schema constraints, ranks items, provides explainable reasoning, and incorporates interactive feedback refinement.

---

## 📌 Overview

The **Personalized Recommendation & Explanation System** demonstrates explainable AI (XAI) and user-in-the-loop adaptation. Rather than delivering black-box predictions, the system explains *why* each resource was selected and adapts dynamically when user feedback is provided.

### Key Modules & Capabilities
1. **User Profile Ingestion (`input_module.py`)**: Gathers attributes including background, interests, current skill level, format preference, target goals, and desired number of recommendations.
2. **Profile Analysis (`profile_module.py`)**: Parses demographic and preference signals to build a unified learner persona.
3. **Intent Detection (`intent_module.py`)**: Infers specific learning pathways (e.g., certification, career pivot, practical project).
4. **Constrained Prompt Generation (`prompt_module.py`)**: Constructs system prompts strictly instructing the model to generate machine-readable JSON schemas.
5. **Recommendation Generation (`recommendation_module.py`)**: Uses **Ollama (`llama3.2`)** with `format="json"` mode to produce structured lists of recommendations with confidence/match scores and explanatory reasons.
6. **Ranking Module (`ranking_module.py`)**: Sorts candidates hierarchically by match scores (0–100%).
7. **Transparent Explanation (`explanation_module.py`)**: Formats human-readable justifications for every recommendation.
8. **Feedback Refinement (`feedback_module.py`)**: Takes user critiques or approval ratings and re-ranks or swaps recommendations accordingly.
9. **Persistence (`save_module.py`)**: Persists curated results into `recommendations.txt`.
10. **Dual Modes**: Complete web interface (`app.py`) and interactive terminal CLI (`main.py`).

---

## 📁 Project Structure

```text
exp_4/GPT_4_Exp_4-main/
├── app.py                     # Flask web application
├── main.py                    # Command-line interactive execution
├── input_module.py            # User profile data collection
├── profile_module.py          # Profile analysis and feature extraction
├── intent_module.py           # User intent classification
├── prompt_module.py           # Structured prompt construction
├── recommendation_module.py   # Ollama JSON recommendation engine
├── ranking_module.py          # Score sorting and prioritization
├── explanation_module.py      # Reasoning and transparency output
├── feedback_module.py         # Human-in-the-loop iterative refinement
├── save_module.py             # Exporting output results
├── recommendations.txt        # Persisted recommendation logs
├── templates/
│   └── index.html             # Web UI template
├── static/
│   ├── script.js              # Web client logic
│   └── style.css              # Custom styling
└── README.md                  # Documentation
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
   cd exp_4/GPT_4_Exp_4-main
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

5. **Run via Web App**:
   ```bash
   python app.py
   ```
   Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

6. **Or Run via CLI**:
   ```bash
   python main.py
   ```

---

## 🔄 Execution Pipeline

```text
   [ User Profile Input ]
             │
             ▼
   [ Profile Analysis & Intent ]
             │
             ▼
   [ Structured Prompt Builder ]
             │
             ▼
[ Ollama (JSON Mode: llama3.2) ]
             │
             ▼
    [ Candidate Ranking ]
             │
             ▼
  [ Transparent Explanation ]
             │
             ▼
[ Feedback Loop & Refinement ]
             │
             ▼
[ Save (recommendations.txt) ]
```

