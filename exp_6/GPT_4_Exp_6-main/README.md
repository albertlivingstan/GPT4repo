# Experiment 6: AI-Powered Medical Symptom Checker & Clinical Decision Support Assistant

A clinical decision support prototype designed to assist in structured anamnesis, symptom extraction, missing clinical context detection, differential causes exploration, and safe patient triage.

---

## 📌 Overview

Medical self-triage applications require stringent safeguards, disclaimers, and structured data handling to avoid hallucinated diagnoses. **Experiment 6** establishes a multi-layered healthcare assistant that emphasizes safety, follow-up inquiry, and non-prescriptive medical guidance.

### Key Modules & Capabilities
1. **Patient Intake (`input_module.py`)**: Gathers demographics (age, biological sex, pregnant/nursing status), primary complaints, symptom duration, severity scale, preexisting conditions, and active medications.
2. **Clinical Profile Formatting (`profile_module.py`)**: Normalizes input data into structured clinical summaries.
3. **Symptom Parsing (`symptom_module.py`)**: Uses keyword recognition and NLP extraction to isolate specific symptoms (e.g., headache, fever, fatigue).
4. **Missing Context Detection (`context_module.py`)**: Checks for critical omissions (such as onset trajectory, pain severity rating, medication allergies, or pregnancy status).
5. **Prompt Engineering (`prompt_module.py`)**: Crafts constrained prompts instructing models to avoid authoritative diagnosis and prioritize patient safety.
6. **Differential Analysis (`analysis_module.py`)**:
   - Queries **OpenAI (`gpt-4`)** if `OPENAI_API_KEY` is present.
   - Gracefully falls back to a deterministic, conservative demonstration analysis when offline or when no API key is configured.
7. **Dynamic Follow-Up Inquiries (`question_module.py`)**: Formulates targeted medical history follow-up questions to clarify vague symptoms.
8. **Clinical Safety & Triage (`safety_module.py`)**:
   - Red flag detection for immediate emergency care (e.g., chest pain, shortness of breath, sudden numbness).
   - Mandatory disclaimer: *"Informational assistance only, not medical diagnosis or prescription."*
9. **Case Report Generation (`save_module.py`)**: Writes comprehensive consultation records to `outputs/medical_analysis.txt`.
10. **Dual Interfaces**: Full web app (`app.py` with `templates/index.html` and `result.html`) and terminal CLI (`main.py`).

---

## 📁 Project Structure

```text
exp_6/GPT_4_Exp_6-main/
├── app.py                     # Flask web application
├── main.py                    # Command-line interactive driver
├── input_module.py            # Patient symptom & demographics intake
├── profile_module.py          # Clinical profile formatter
├── symptom_module.py          # Symptom extraction logic
├── context_module.py          # Missing diagnostic context detector
├── prompt_module.py           # Guardrailed LLM prompt generator
├── analysis_module.py         # GPT-4 / local fallback analysis
├── question_module.py         # Anamnesis follow-up question generator
├── safety_module.py           # Emergency triage checks & disclaimers
├── save_module.py             # Exporting patient reports
├── utils.py                   # Formatting utilities
├── requirements.txt           # Dependency list
├── data/
│   └── sample_cases.csv       # Benchmark clinical scenarios
├── outputs/
│   └── medical_analysis.txt   # Exported clinical summaries
├── templates/
│   ├── index.html             # Patient symptom input form
│   └── result.html            # Structured medical report display
├── static/
│   └── style.css              # Healthcare UI theme
└── README.md                  # Documentation
```

---

## 🛠️ Prerequisites & Configuration

1. **Python 3.10+**
2. **OpenAI API Key (Optional)**:
   - If configured, the app communicates with OpenAI's `gpt-4` model.
   - If not set, the app continues functioning using built-in clinical fallback responses.
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   export OPENAI_MODEL="gpt-4" # Optional, defaults to gpt-4
   ```

---

## 🚀 Installation & Setup

1. **Navigate to the experiment directory**:
   ```bash
   cd exp_6/GPT_4_Exp_6-main
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
   pip install flask pandas
   ```

4. **Run via Web Application**:
   ```bash
   python app.py
   ```
   Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

5. **Or Run via CLI**:
   ```bash
   python main.py
   ```

---

## ⚠️ Medical Disclaimer

This project is created strictly for academic and educational purposes under the curriculum **Building Applications using GPT-4 / LLMs**. It does not provide medical diagnosis, treatment advice, or prescriptions. Patients experiencing acute medical distress must contact emergency services immediately.

