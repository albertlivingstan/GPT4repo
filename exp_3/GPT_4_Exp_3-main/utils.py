from datetime import datetime
import os

def save_reply(email, reply, intent):
    os.makedirs("outputs", exist_ok=True)

    with open("outputs/generated_reply.txt", "a", encoding="utf-8") as file:
        file.write(f"Date: {datetime.now()}\n")
        file.write(f"Customer Email: {email}\n")
        file.write(f"Intent: {intent}\n")
        file.write(f"Generated Reply: {reply}\n")
        file.write("-" * 40 + "\n")