def extract_symptoms(text):
    """Extract symptoms from natural-language input."""

    known_symptoms = [
        "fever",
        "cough",
        "sore throat",
        "headache",
        "runny nose",
        "fatigue",
        "nausea",
        "vomiting",
        "diarrhea",
        "dizziness",
        "chest pain",
        "shortness of breath",
        "difficulty breathing",
        "body aches",
        "rash"
    ]

    text = text.lower()
    extracted = []

    for symptom in known_symptoms:
        if symptom in text:
            extracted.append(symptom.title())

    return extracted