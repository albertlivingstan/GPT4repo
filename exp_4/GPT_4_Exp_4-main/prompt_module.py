def create_prompt(profile):
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

Recommend {profile['num_items']} suitable learning resources.

For each recommendation provide:
1. Name
2. Reason
3. Suitability score
"""

    return prompt