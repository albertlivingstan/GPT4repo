import requests

def improve_tone(reply, tone):
    prompt = f"Rewrite this email in a {tone} tone:\n{reply}"

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3.2", "prompt": prompt, "stream": False}
    )

    return response.json()["response"].strip()