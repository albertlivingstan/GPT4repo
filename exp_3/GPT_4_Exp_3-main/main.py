from input_module import get_customer_details, display_customer_details
from intent_module import detect_intent
from retrieval_module import retrieve_similar_email
from reply_module import generate_reply
from tone_module import improve_tone
from summary_module import summarize_email
from utils import save_reply


def main():
    while True:
        print("\n===== Intelligent Email Assistant =====")
        print("1. Process Customer Email")
        print("2. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            details = get_customer_details()
            display_customer_details(details)

            email = details["customer_email"]

            intent = detect_intent(email)
            print("\nDetected Intent:", intent)

            similar = retrieve_similar_email(email)
            print("\nPrevious Email:", similar["previous_email"])
            print("Previous Reply:", similar["previous_reply"])

            reply = generate_reply(email, similar["previous_reply"])
            print("\nGenerated Reply:\n", reply)

            tone = input(
                "\nChoose tone (Friendly/Formal/Empathetic): "
            )
            improved = improve_tone(reply, tone)
            print("\nImproved Reply:\n", improved)

            print("\nSummary:\n", summarize_email(email))

            save_reply(email, improved, intent)
            print("\nReply saved successfully.")

        elif choice == "2":
            print("Thank you!")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()