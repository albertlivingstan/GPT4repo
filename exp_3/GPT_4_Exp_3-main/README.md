# Experiment 3: Intelligent Customer Email Assistant

A multi-module AI assistant that processes customer emails, identifies business intent, retrieves similar historical queries, drafts context-aware responses, adapts writing tone, and summarizes conversations.

---

## 📌 Overview

The **Intelligent Customer Email Assistant** demonstrates an end-to-end customer support automation workflow. It combines rule-based classification, dataset retrieval (few-shot context matching), and local Large Language Model (LLM) generation using **Ollama (`llama3.2`)**.

### Key Modules & Capabilities
1. **Customer Ingestion (`input_module.py`)**: Captures customer metadata (name, subject, email body).
2. **Intent Classification (`intent_module.py`)**: Categorizes emails into:
   - `Delivery Issue`
   - `Refund Request`
   - `Product Complaint`
   - `Technical Support`
   - `Order Cancellation`
   - `General Inquiry`
3. **Retrieval Module (`retrieval_module.py`)**: Searches historical interactions from `data/emails.csv` to find contextually relevant past resolutions.
4. **Context-Aware Reply Generation (`reply_module.py`)**: Leverages retrieved precedent and prompt engineering to compose an initial draft.
5. **Tone Customization (`tone_module.py`)**: Rewrites replies according to selected persona:
   - `Friendly`
   - `Formal` / `Professional`
   - `Empathetic`
6. **Executive Summarization (`summary_module.py`)**: Produces a concise summary for support ticketing and internal audit.
7. **Persistence (`utils.py`)**: Archives drafted responses to `outputs/generated_reply.txt`.
8. **Dual Interfaces**: Offers both a command-line interface (`main.py`) and a full web application (`app.py`).

---

## 📁 Project Structure

```text
exp_3/GPT_4_Exp_3-main/
├── app.py                # Flask web application & REST routes
├── main.py               # Interactive CLI driver
├── input_module.py       # Customer data intake
├── intent_module.py      # LLM-based intent recognition
├── retrieval_module.py   # Historical dataset lookup
├── reply_module.py       # Draft generation logic
├── tone_module.py        # Tone adjustment engine
├── summary_module.py     # Email summarization
├── utils.py              # File output and utility helpers
├── data/
│   └── emails.csv        # Precedent customer interactions & resolutions
├── outputs/
│   └── generated_reply.txt # Saved responses and summaries
├── templates/
│   └── index.html        # Web interface template
├── static/
│   └── style.css         # UI stylesheet
└── README.md             # Experiment documentation
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
   cd exp_3/GPT_4_Exp_3-main
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
   pip install flask pandas requests
   ```

4. **Ensure Ollama service is active**:
   ```bash
   ollama serve
   ```

5. **Run via Web Application**:
   ```bash
   python app.py
   ```
   Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

6. **Or Run via Interactive CLI**:
   ```bash
   python main.py
   ```

---

## 📊 Workflow Diagram

```text
               [ Customer Email ]
                       │
         ┌─────────────┴─────────────┐
         ▼                           ▼
[ Intent Detection ]     [ Historical Retrieval ]
(llama3.2 classification)  (data/emails.csv match)
         └─────────────┬─────────────┘
                       ▼
            [ Reply Generation ]
          (Context-Augmented Draft)
                       │
                       ▼
           [ Tone Modification ]
        (Friendly / Formal / Empathetic)
                       │
         ┌─────────────┴─────────────┐
         ▼                           ▼
[ Executive Summary ]       [ Output Storage ]
  (Short Briefing)         (outputs/generated_reply.txt)
```

