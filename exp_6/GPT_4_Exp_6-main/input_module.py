def collect_patient_information():
    """Collect patient information from the user."""

    patient = {}

    patient["age"] = input("Enter age: ")
    patient["sex"] = input("Enter sex: ")
    patient["symptoms_text"] = input("Enter symptoms: ")
    patient["duration"] = input("Duration of symptoms: ")
    patient["severity"] = input("Severity (Mild/Moderate/Severe): ")
    patient["history"] = input("Medical history: ")
    patient["medications"] = input("Current medications: ")
    patient["allergies"] = input("Allergies: ")

    return patient