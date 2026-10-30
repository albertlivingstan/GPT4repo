def build_analysis_prompt(patient, symptoms, missing):
    """Construct the GPT-4 prompt."""

    prompt = f"""
You are a medical information assistant.

Analyze the provided symptoms cautiously.

Do not provide a definitive diagnosis or prescribe medication.
Do not invent information.
Explain possible causes in simple language.
Ask relevant follow-up questions.
Recommend professional medical attention when appropriate.

Patient Information:
Age: {patient.get('age')}
Sex: {patient.get('sex')}
Duration: {patient.get('duration')}
Severity: {patient.get('severity')}
Medical History: {patient.get('history')}
Medications: {patient.get('medications')}
Allergies: {patient.get('allergies')}

Reported Symptoms:
{patient.get('symptoms_text')}

Extracted Symptoms:
{', '.join(symptoms)}

Missing Information:
{', '.join(missing)}

Provide these sections:
1. Possible Conditions
2. Explanation
3. Follow-up Questions
4. Medical Attention Guidance

Clearly state that the response is not a medical diagnosis.
"""

    return prompt