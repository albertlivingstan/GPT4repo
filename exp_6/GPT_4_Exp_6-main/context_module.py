def find_missing_information(patient):
    """Identify missing information."""

    missing = []

    if not patient.get("age"):
        missing.append("Age")

    if not patient.get("duration"):
        missing.append("Symptom duration")

    if not patient.get("severity"):
        missing.append("Symptom severity")

    symptoms = patient.get("symptoms_text", "").lower()

    if "fever" in symptoms and "temperature" not in symptoms:
        missing.append("Measured temperature")

    if not symptoms:
        missing.append("Symptom description")

    return missing