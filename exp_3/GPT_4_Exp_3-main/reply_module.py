import requests

def generate_reply(email, previous_reply):
    prompt = f"""
    Write a professional customer support email reply.
    Customer email: {email}
    Previous reply for reference: {previous_reply}
    """

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3.2", "prompt": prompt, "stream": False}
    )

    return response.json()["response"].strip()