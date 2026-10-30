import os


def generate_analysis(prompt, symptoms, missing):
    """Generate symptom analysis using GPT-4 when available."""

    api_key = os.getenv("OPENAI_API_KEY")

    if api_key:
        try:
            from openai import OpenAI

            client = OpenAI(api_key=api_key)

            response = client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4"),
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Provide cautious general health information. "
                            "Do not diagnose or prescribe medication."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.2
            )

            return {
                "Possible Conditions and Analysis":
                    response.choices[0].message.content
            }

        except Exception as error:
            print("API error:", error)
            print("Using demonstration output.")

    return {
        "Possible Conditions and Analysis": (
            "The symptoms may have several possible causes. "
            "The available information is insufficient to establish "
            "a diagnosis. Consult a qualified healthcare professional "
            "for an appropriate assessment.\n\n"
            "Missing information: "
            + (", ".join(missing) if missing else "None detected")
        )
    }