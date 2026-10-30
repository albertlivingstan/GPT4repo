# Experiment 5: Automated Legal Document Analyzer

An AI-powered legal document review system built with **Streamlit**, **PyPDF**, and **Ollama (`llama3.2:3b`)**. Extracts key clauses, analyzes contractual risks, answers questions over uploaded agreements, and generates structured legal reports.

---

## 📌 Overview

Legal agreements and contracts are lengthy, jargon-dense, and time-consuming to audit manually. The **Automated Legal Document Analyzer** accelerates the review process by parsing plain text (`.txt`) or PDF (`.pdf`) files and extracting critical contractual elements through a locally running LLM.

### Key Capabilities
- **Multi-Format Ingestion**: Supports direct upload and text extraction from both `.pdf` and `.txt` documents using `pypdf`.
- **Text Normalization**: Strips null bytes, normalizes whitespace, and cleans up document flow.
- **11-Point Structured Analysis**:
  1. Document Type
  2. Parties Involved
  3. Purpose & Recitals
  4. Executive Summary
  5. Mutual Obligations
  6. Financial / Payment Terms
  7. Term & Duration
  8. Termination Conditions
  9. Key Dates & Deadlines
  10. Critical Clauses (e.g., Indemnity, Confidentiality, Jurisdiction)
  11. Potential Risks & Ambiguities
- **Interactive Document Q&A**: Lets users ask specific ad-hoc questions regarding the uploaded contract.
- **Timestamped Audit Export**: Saves structured analysis reports automatically to `outputs/legal_analysis_<timestamp>.txt`.
- **Legal Compliance Warning**: Displays prominent disclaimers advising that the tool provides informational analysis rather than binding legal counsel.

---

## 📁 Project Structure

```text
exp_5/GPT_4_Exp_5-main/
├── app.py                # Streamlit web application & analysis pipeline
├── requirements.txt      # Dependency specification
├── outputs/              # Generated legal audit text reports
│   └── legal_analysis_*.txt
└── README.md             # Experiment documentation
```

---

## 🛠️ Prerequisites

1. **Python 3.10+**
2. **Ollama**: [Download & install Ollama](https://ollama.com/)
3. **Llama 3.2 3B Model**:
   ```bash
   ollama pull llama3.2:3b
   ```

---

## 🚀 Installation & Setup

1. **Navigate to the experiment directory**:
   ```bash
   cd exp_5/GPT_4_Exp_5-main
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
   pip install -r requirements.txt
   ```

4. **Verify Ollama is running**:
   ```bash
   ollama serve
   ```

5. **Run the Streamlit application**:
   ```bash
   streamlit run app.py
   ```

6. **Open in browser**:
   Streamlit will automatically open [http://localhost:8501](http://localhost:8501).

---

## 📑 Sample Analysis Output

```text
============================================================
           AUTOMATED LEGAL DOCUMENT ANALYSIS REPORT
============================================================
Analysis Date: 2026-10-30 22:30:00
Source File: Non_Disclosure_Agreement.pdf
AI Model: Ollama | Llama 3.2 (3B)

1. Document Type: Non-Disclosure Agreement (Mutual)
2. Parties: Acme Corp and Beta LLC
3. Purpose: Exploration of a potential joint venture...
...
11. Risks or Ambiguities:
    - Ambiguous definition of "Derived Data" in Section 4.2
    - Unilateral indemnity obligations favor Disclosing Party
============================================================
```

