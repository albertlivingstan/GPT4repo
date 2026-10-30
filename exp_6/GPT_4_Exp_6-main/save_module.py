from pathlib import Path
from datetime import datetime


OUTPUT_FILE = (
    Path(__file__).resolve().parent
    / "outputs"
    / "medical_analysis.txt"
)


def save_report(report):
    """Save the generated report to a text file."""

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        file.write("AI-POWERED MEDICAL SYMPTOM ASSISTANT\n")
        file.write(
            "Generated: "
            + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            + "\n\n"
        )

        for heading, content in report.items():
            file.write(heading.upper() + "\n")
            file.write("-" * 40 + "\n")
            file.write(str(content) + "\n\n")

    return OUTPUT_FILE