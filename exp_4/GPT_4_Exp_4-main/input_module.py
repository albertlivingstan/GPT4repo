def collect_user_profile():
    print("\n===== USER PROFILE =====")

    name = input("Enter your name: ")
    age = input("Enter your age: ")
    background = input("Enter your educational/professional background: ")
    interests = input("Enter your interests: ")
    skill_level = input("Enter your skill level: ")
    preference = input("Enter your preferred category/type: ")
    goal = input("Enter your goal: ")
    num_items = int(input("Enter number of recommendations required: "))

    profile = {
        "name": name,
        "age": age,
        "background": background,
        "interests": interests,
        "skill_level": skill_level,
        "preference": preference,
        "goal": goal,
        "num_items": num_items
    }

    return profile