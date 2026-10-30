import requests

def detect_intent(email):
    prompt = f"""
    Classify this customer email into exactly one category:
    Delivery Issue, Refund Request, Product Complaint,
    Technical Support, Order Cancellation, General Inquiry.

    Email: {email}
    Return only the category.
    """

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3.2", "prompt": prompt, "stream": False}
    )

    return response.json()["response"].strip()