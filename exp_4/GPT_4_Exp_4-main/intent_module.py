def detect_intent(user_input):
    text = user_input.lower().strip()

    if "exit" in text or "quit" in text or "bye" in text:
        return "EXIT"

    elif "save" in text:
        return "SAVE_RECOMMENDATION"

    elif "profile" in text or "my details" in text:
        return "SHOW_PROFILE"

    elif "why" in text or "explain" in text or "reason" in text:
        return "EXPLAIN_RECOMMENDATION"

    elif "refine" in text or "change" in text or "more suitable" in text:
        return "REFINE_RECOMMENDATION"

    elif "recommend" in text or "suggest" in text:
        return "GENERATE_RECOMMENDATION"

    else:
        return "UNKNOWN"