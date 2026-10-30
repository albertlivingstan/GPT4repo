import ollama
import json


def generate_recommendations(profile):

    prompt = f"""
You are a personalized recommendation assistant.

User Profile:
Name: {profile['name']}
Age: {profile['age']}
Background: {profile['background']}
Interests: {profile['interests']}
Skill Level: {profile['skill_level']}
Preference: {profile['preference']}
Goal: {profile['goal']}

Recommend exactly {profile['num_items']} suitable learning resources.

Return ONLY valid JSON in this format:

{{
    "recommendations": [
        {{
            "name": "Resource name",
            "score": 95,
            "reason": "Why this resource suits the user"
        }}
    ]
}}

The score must be a number from 0 to 100.
Do not include any text outside the JSON.
"""

    response = ollama.chat(
        model="llama3.2:latest",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        format="json"
    )

    result = json.loads(response["message"]["content"])

    recommendations = result["recommendations"]

    return recommendations