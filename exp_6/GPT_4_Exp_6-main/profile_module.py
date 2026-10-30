def format_patient_profile(patient):
    """Format patient information for the report."""

    return (
        f"Age: {patient.get('age', 'Not provided')}\n"
        f"Sex: {patient.get('sex', 'Not provided')}\n"
        f"Duration: {patient.get('duration', 'Not provided')}\n"
        f"Severity: {patient.get('severity', 'Not provided')}\n"
        f"Medical History: {patient.get('history', 'Not provided')}\n"
        f"Medications: {patient.get('medications', 'Not provided')}\n"
        f"Allergies: {patient.get('allergies', 'Not provided')}"
    )