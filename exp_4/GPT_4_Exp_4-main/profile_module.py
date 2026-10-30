def analyze_profile(profile):
    print("\n===== PREFERENCE ANALYSIS =====")
    print("--------------------------------")

    interests = profile["interests"].split(",")

    primary_interest = interests[0].strip()

    if len(interests) > 1:
        secondary_interest = interests[1].strip()
    else:
        secondary_interest = "None"

    print("Primary Interest :", primary_interest)
    print("Secondary Interest :", secondary_interest)
    print("Skill Level :", profile["skill_level"])
    print("Goal :", profile["goal"])
    print("Preference :", profile["preference"])

    return {
        "primary_interest": primary_interest,
        "secondary_interest": secondary_interest,
        "skill_level": profile["skill_level"],
        "goal": profile["goal"],
        "preference": profile["preference"]
    }