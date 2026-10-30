import ollama
import json


def refine_recommendations(profile, feedback):

    prompt = f"""
You are a personalized recommendation assistant.

Original User Profile:
Name: {profile['name']}
Age: {profile['age']}
Background: {profile['background']}
Interests: {profile['interests']}
Skill Level: {profile['skill_level']}
Preference: {profile['preference']}
Goal: {profile['goal']}

User Feedback:
{feedback}

Based on the user's feedback, generate exactly {profile['num_items']} refined
learning recommendations.

Return ONLY valid JSON in this format:

{{
    "recommendations": [
        {{
            "name": "Resource name",
            "score": 95,
            "reason": "Why this resource now suits the user"
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

    return result["recommendations"]


def get_feedback():
    print("\n===== USER FEEDBACK =====")

    feedback = input(
        "Enter your feedback about the recommendations: "
    )

    return feedback