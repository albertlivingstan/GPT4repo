import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def retrieve_similar_email(email):
    df = pd.read_csv("data/emails.csv")

    vectorizer = TfidfVectorizer()
    texts = df["Customer_Email"].fillna("").tolist()
    matrix = vectorizer.fit_transform(texts + [email])

    similarities = cosine_similarity(matrix[-1], matrix[:-1])[0]
    index = similarities.argmax()

    return {
        "previous_email": df.iloc[index]["Customer_Email"],
        "previous_reply": df.iloc[index]["Previous_Reply"]
    }