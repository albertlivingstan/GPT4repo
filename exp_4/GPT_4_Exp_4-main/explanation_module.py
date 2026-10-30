def show_explanations(recommendations):
    print("\n===== RECOMMENDATION EXPLANATIONS =====")
    print("---------------------------------------")

    for i, item in enumerate(recommendations, start=1):
        print(f"\n{i}. {item['name']}")
        print(f"Score: {item['score']}%")
        print(f"Reason: {item['reason']}")