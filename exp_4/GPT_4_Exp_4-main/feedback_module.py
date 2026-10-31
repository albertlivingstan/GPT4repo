import json
from recommendation_module import ask_ollama_json


def refine_recommendations(profile, feedback):
    prompt = f"""You are PathFinder AI, an elite personalized learning curriculum engine.

Original User Profile:
Name: {profile.get('name', 'Learner')}
Age: {profile.get('age', 'N/A')}
Background: {profile.get('background', 'N/A')}
Interests: {profile.get('interests', 'N/A')}
Skill Level: {profile.get('skill_level', 'N/A')}
Preference: {profile.get('preference', 'N/A')}
Goal: {profile.get('goal', 'N/A')}

User Feedback & Refinement Critique:
"{feedback}"

Based on this specific feedback, adapt and regenerate exactly {profile.get('num_items', 4)} refined learning recommendations that directly address the user's critique.

Return ONLY valid JSON in this exact structure:
{{
    "recommendations": [
        {{
            "name": "Resource Name",
            "type": "Course / Project / Book / Certification",
            "score": 96,
            "difficulty": "Beginner / Intermediate / Advanced",
            "reason": "Why this resource satisfies the user's refinement feedback."
        }}
    ]
}}

The score must be a number from 70 to 99.
Return ONLY the raw JSON object."""

    result = ask_ollama_json(prompt)
    return result.get("recommendations", [])


def get_feedback():
    print("\n===== USER FEEDBACK =====")
    return input("How would you like to refine these recommendations? ")
