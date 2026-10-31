
import os
from flask import Flask, render_template, request
from analysis_module import generate_analysis
from pathlib import Path

app = Flask(__name__)

OUTPUT_FILE = Path(__file__).parent / "outputs" / "medical_analysis.txt"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    age = request.form.get("age", "").strip()
    sex = request.form.get("sex", "").strip()
    symptoms = request.form.get("symptoms", "").strip()
    duration = request.form.get("duration", "").strip()
    severity = request.form.get("severity", "").strip()

    if not symptoms:
        return render_template(
            "index.html",
            error="Please enter your symptoms."
        )

    patient_info = (
        f"Age: {age}\n"
        f"Sex: {sex or 'Not provided'}\n"
        f"Symptoms: {symptoms}\n"
        f"Duration: {duration or 'Not provided'}\n"
        f"Severity: {severity or 'Not provided'}"
    )

    missing = []
    if not age:
        missing.append("Age")
    if not sex:
        missing.append("Sex, if relevant")
    if not duration:
        missing.append("Symptom duration")
    if not severity:
        missing.append("Symptom severity")

    prompt = f"""
You are an educational medical symptom information assistant.

Provide cautious general health information, not a diagnosis.
Do not prescribe medication or invent patient details.
Explain that symptoms can have multiple causes.
Mention relevant warning signs and when professional care is needed.
If information is missing, state what further information may help.

Patient information:
{patient_info}

Missing information:
{", ".join(missing) if missing else "None identified"}
"""

    result = generate_analysis(prompt, symptoms, missing)
    analysis = result.get(
        "Possible Conditions and Analysis",
        "No analysis was returned."
    )

    report = f"""
MEDICAL SYMPTOM ASSISTANT REPORT
================================

{patient_info}

POSSIBLE CONDITIONS AND ANALYSIS
--------------------------------
{analysis}

DISCLAIMER
----------
Educational information only. This is not a diagnosis or a substitute
for professional medical advice.
"""

    save_message = "Report saved successfully."

    try:
        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_FILE.write_text(report, encoding="utf-8")
    except OSError as error:
        print("Report saving error:", error)
        save_message = "Analysis displayed, but report saving failed."

    return render_template(
        "result.html",
        age=age,
        sex=sex,
        symptoms=symptoms,
        duration=duration,
        severity=severity,
        analysis=analysis,
        save_message=save_message
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5006))
    app.run(debug=True, port=port)
