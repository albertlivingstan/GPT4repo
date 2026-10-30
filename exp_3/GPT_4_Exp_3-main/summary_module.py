import requests

def summarize_email(email):
    prompt = f"Summarize this customer issue in 50 words:\n{email}"

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3.2", "prompt": prompt, "stream": False}
    )

    return response.json()["response"].strip()