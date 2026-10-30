def rank_recommendations(recommendations):
    ranked = sorted(
        recommendations,
        key=lambda x: x["score"],
        reverse=True
    )

    print("\n===== RANKED RECOMMENDATIONS =====")
    print("----------------------------------")
    print("Rank | Recommendation | Score")
    print("----------------------------------")

    for rank, item in enumerate(ranked, start=1):
        print(f"{rank} | {item['name']} | {item['score']}%")

    return ranked