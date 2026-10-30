DISCLAIMER = """
This AI-generated response is intended for educational
and informational purposes only.

It is not a medical diagnosis and does not replace advice
from a qualified healthcare professional.

For serious, worsening or urgent symptoms, seek
appropriate medical care.
"""


def medical_attention_guidance(symptoms):
    """Display cautious medical-attention guidance."""

    symptoms = symptoms.lower()

    warning_signs = [
        "difficulty breathing",
        "shortness of breath",
        "severe chest pain",
        "unconscious",
        "severe bleeding"
    ]

    for sign in warning_signs:
        if sign in symptoms:
            return (
                "A potentially serious warning sign was mentioned. "
                "Seek urgent medical help now or contact your local "
                "emergency number. This program cannot make a clinical "
                "triage decision."
            )

    return (
        "If symptoms are severe, rapidly worsening, persistent "
        "or concerning, contact a qualified healthcare professional. "
        "Seek emergency help for potentially life-threatening symptoms."
    )