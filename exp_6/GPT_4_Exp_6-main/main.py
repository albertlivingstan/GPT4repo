from input_module import collect_patient_information
from profile_module import format_patient_profile
from symptom_module import extract_symptoms
from context_module import find_missing_information
from prompt_module import build_analysis_prompt
from analysis_module import generate_analysis
from question_module import generate_follow_up_questions
from safety_module import medical_attention_guidance, DISCLAIMER
from save_module import save_report
from utils import print_section


def create_report(patient):
    """Combine all modules into a structured report."""

    symptoms = extract_symptoms(
        patient.get("symptoms_text", "")
    )

    missing = find_missing_information(patient)

    prompt = build_analysis_prompt(
        patient, symptoms, missing
    )

    analysis = generate_analysis(
        prompt, symptoms, missing
    )

    questions = generate_follow_up_questions()

    report = {
        "Reported Symptoms": (
            ", ".join(symptoms)
            if symptoms
            else patient.get("symptoms_text", "Not specified")
        ),

        "Patient Information": format_patient_profile(patient),

        "Possible Conditions": analysis[
            "Possible Conditions and Analysis"
        ],

        "Explanation": (
            "Symptoms can have multiple causes. "
            "This application cannot establish a diagnosis."
        ),

        "Missing Information": (
            "\n".join(missing)
            if missing
            else "No missing information detected by basic checks."
        ),

        "Follow-up Questions": "\n".join(
            f"{i}. {question}"
            for i, question in enumerate(questions, 1)
        ),

        "Medical Attention Guidance": medical_attention_guidance(
            patient.get("symptoms_text", "")
        ),

        "Disclaimer": DISCLAIMER
    }

    return report


def main():
    patient = {}
    report = None

    while True:
        print("\n" + "=" * 55)
        print(" AI-POWERED MEDICAL SYMPTOM ASSISTANT")
        print("=" * 55)

        print("1. Enter Patient Information")
        print("2. Enter Symptoms")
        print("3. Analyze Symptoms")
        print("4. Generate Follow-up Questions")
        print("5. Display Possible Conditions")
        print("6. Display Medical Attention Guidance")
        print("7. Display Disclaimer")
        print("8. Save Report")
        print("9. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            patient = collect_patient_information()
            report = None

            print("\nPatient information collected successfully.")

        elif choice == "2":
            if not patient:
                print("Please enter patient information first.")
                continue

            patient["symptoms_text"] = input(
                "Describe your symptoms: "
            ).strip()

            report = None
            print("Symptoms recorded.")

        elif choice in ["3", "4", "5", "6", "8"]:
            if not patient:
                print("Please choose option 1 first.")
                continue

            if not patient.get("symptoms_text"):
                patient["symptoms_text"] = input(
                    "Describe your symptoms: "
                ).strip()

            if not patient["symptoms_text"]:
                print("Please enter your symptoms.")
                continue

            report = create_report(patient)

            if choice == "3":
                for title, content in report.items():
                    print_section(title, content)

            elif choice == "4":
                print_section(
                    "Follow-up Questions",
                    report["Follow-up Questions"]
                )

            elif choice == "5":
                print_section(
                    "Possible Conditions",
                    report["Possible Conditions"]
                )

            elif choice == "6":
                print_section(
                    "Medical Attention Guidance",
                    report["Medical Attention Guidance"]
                )

            elif choice == "8":
                path = save_report(report)
                print(f"\nReport saved successfully to:\n{path}")

        elif choice == "7":
            print_section("Disclaimer", DISCLAIMER)

        elif choice == "9":
            print("Thank you for using the application!")
            break

        else:
            print("Invalid choice. Enter a number from 1 to 9.")


if __name__ == "__main__":
    main()