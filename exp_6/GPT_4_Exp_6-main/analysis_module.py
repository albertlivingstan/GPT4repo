import os


def generate_analysis(prompt, symptoms, missing):
    """Generate symptom analysis using OpenAI GPT-4 or local Ollama LLM."""

    # 1. Try OpenAI if API key is provided
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
                            "Provide cautious, structured health information. "
                            "Do not diagnose or prescribe medication. "
                            "Highlight potential differential considerations, red flags, and triage urgency."
                        )
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2
            )
            return {
                "Possible Conditions and Analysis": response.choices[0].message.content
            }
        except Exception as error:
            print("OpenAI API error:", error)

    # 2. Try Local Ollama (llama3.2 or llama3.2:3b)
    try:
        import ollama
        models_to_try = [os.getenv("OLLAMA_MODEL", "llama3.2"), "llama3.2:3b", "llama3.2:latest"]
        for model_name in dict.fromkeys(models_to_try):
            try:
                response = ollama.chat(
                    model=model_name,
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are an educational medical clinical support assistant. "
                                "Provide cautious, structured health information. "
                                "Do not formulate definitive diagnoses or prescribe medication. "
                                "Format your response with clear sections: "
                                "1. Clinical Overview, 2. Potential Differential Considerations, "
                                "3. Critical Red Flag Warnings, 4. Recommended Next Steps for Medical Consultation."
                            )
                        },
                        {"role": "user", "content": prompt}
                    ]
                )
                content = response.get("message", {}).get("content", "").strip()
                if content:
                    return {"Possible Conditions and Analysis": content}
            except Exception as e:
                if "not found" in str(e).lower():
                    continue
                raise
    except Exception as ollama_err:
        print("Ollama local analysis error:", ollama_err)

    # 3. Deterministic Clinical Fallback
    return {
        "Possible Conditions and Analysis": (
            "Clinical Assessment Summary:\n\n"
            "The reported symptoms may be associated with various common benign etiologies or early viral syndromes. "
            "However, self-reported symptoms are insufficient to establish a medical diagnosis.\n\n"
            "Key Missing Information:\n"
            + ("• " + "\n• ".join(missing) if missing else "• None detected by basic triage.")
            + "\n\nRecommendations:\n"
            "1. Monitor symptom progression, body temperature, and hydration levels.\n"
            "2. Seek immediate emergency evaluation if you experience chest pain, sudden breathlessness, severe dizzy spells, or high unrelenting fever.\n"
            "3. Schedule an in-person appointment with a primary care physician for diagnostic evaluation."
        )
    }
