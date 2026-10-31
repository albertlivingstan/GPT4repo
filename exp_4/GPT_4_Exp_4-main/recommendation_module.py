import ollama
import json

FALLBACK_MODELS = ["llama3.2:latest", "llama3.2", "llama3.2:3b", "qwen2.5:3b"]


def ask_ollama_json(prompt):
    last_err = None
    for model_name in FALLBACK_MODELS:
        try:
            response = ollama.chat(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                format="json"
            )
            content = response.get("message", {}).get("content", "").strip()
            return json.loads(content)
        except Exception as e:
            last_err = e
            if "not found" in str(e).lower():
                continue
            raise
    if last_err:
        raise last_err
    return {"recommendations": []}


def generate_recommendations(profile):
    prompt = f"""You are PathFinder AI, an elite personalized learning recommendation and curriculum intelligence engine.

User Profile:
Name: {profile['name']}
Age: {profile['age']}
Background: {profile['background']}
Interests: {profile['interests']}
Skill Level: {profile['skill_level']}
Learning Preference: {profile['preference']}
Career/Learning Goal: {profile['goal']}

Recommend exactly {profile['num_items']} top-tier learning resources tailored to this profile.

Return ONLY valid JSON in this exact structure:
{{
    "recommendations": [
        {{
            "name": "Resource Name (Course, Book, Certification, or Project)",
            "type": "Course / Project / Book / Certification",
            "score": 95,
            "difficulty": "Beginner / Intermediate / Advanced",
            "reason": "Clear explanation of why this resource directly advances the user's specific career goal."
        }}
    ]
}}

The score must be an integer between 70 and 99 reflecting alignment percentage.
Do not output any markdown code fences or conversational text outside the JSON object."""

    result = ask_ollama_json(prompt)
    return result.get("recommendations", [])
