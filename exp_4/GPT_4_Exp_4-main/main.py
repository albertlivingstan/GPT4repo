from input_module import collect_user_profile
from profile_module import analyze_profile
from prompt_module import create_prompt
from recommendation_module import generate_recommendations
from ranking_module import rank_recommendations
from explanation_module import show_explanations
from feedback_module import get_feedback, refine_recommendations
from intent_module import detect_intent
from save_module import save_recommendations


def display_profile(profile):
    print("\n===== USER PROFILE =====")
    print("------------------------")
    print("Name :", profile["name"])
    print("Age :", profile["age"])
    print("Background :", profile["background"])
    print("Interests :", profile["interests"])
    print("Skill Level :", profile["skill_level"])
    print("Preference :", profile["preference"])
    print("Goal :", profile["goal"])
    print("No. of Items :", profile["num_items"])


def main():

    print("==========================================")
    print("  PERSONALIZED RECOMMENDATION SYSTEM")
    print("==========================================")

    # Part A - Collect user profile
    profile = collect_user_profile()

    # Display profile
    display_profile(profile)

    # Part B - Analyze preferences
    analysis = analyze_profile(profile)

    # Part C - Create GPT prompt
    prompt = create_prompt(profile)

    print("\n===== GENERATED PROMPT =====")
    print(prompt)

    # Part D - Generate recommendations
    recommendations = generate_recommendations(profile)

    print("\n===== PERSONALIZED RECOMMENDATIONS =====")
    print("----------------------------------------")

    for i, item in enumerate(recommendations, start=1):
        print(f"\n{i}. {item['name']}")
        print(f"Score: {item['score']}%")
        print(f"Reason: {item['reason']}")

    # Part E - Rank recommendations
    recommendations = rank_recommendations(recommendations)

    # Part F - Explanation
    show_explanations(recommendations)

    # Part G and H - Continuous interaction
    while True:

        print("\n================================")
        print("What would you like to do?")
        print("1. Get feedback/refine recommendations")
        print("2. Show profile")
        print("3. Explain recommendations")
        print("4. Save recommendations")
        print("5. Detect intent")
        print("6. Exit")
        print("================================")

        choice = input("Enter your choice: ")

        if choice == "1":

            feedback = get_feedback()

            print("\nYour Feedback:")
            print(feedback)

            recommendations = refine_recommendations(
                profile,
                feedback
            )

            recommendations = rank_recommendations(recommendations)

            print("\n===== REFINED RECOMMENDATIONS =====")
            print("----------------------------------")

            for i, item in enumerate(recommendations, start=1):
                print(f"\n{i}. {item['name']}")
                print(f"Score: {item['score']}%")
                print(f"Reason: {item['reason']}")

            show_explanations(recommendations)

        elif choice == "2":

            display_profile(profile)

        elif choice == "3":

            show_explanations(recommendations)

        elif choice == "4":

            save_recommendations(recommendations)

        elif choice == "5":

            user_input = input("Enter your request: ")

            intent = detect_intent(user_input)

            print("Detected Intent:", intent)

        elif choice == "6":

            print("\nThank you for using the Personalized Recommendation System!")
            break

        else:

            print("\nInvalid choice. Please try again.")


if __name__ == "__main__":
    main()