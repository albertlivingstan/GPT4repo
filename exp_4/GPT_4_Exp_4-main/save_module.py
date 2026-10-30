def save_recommendations(recommendations):
    with open("recommendations.txt", "w") as file:
        file.write("PERSONALIZED RECOMMENDATIONS\n")
        file.write("--------------------------------\n\n")

        for i, item in enumerate(recommendations, start=1):
            file.write(f"{i}. {item['name']}\n")
            file.write(f"Score: {item['score']}%\n")
            file.write(f"Reason: {item['reason']}\n\n")

    print("\nRecommendations saved successfully!")