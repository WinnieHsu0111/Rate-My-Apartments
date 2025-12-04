import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

apartments = pd.read_csv("./data/apartments_master.csv")

def fetch_reviews(place_id):
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "key": API_KEY,
        "reviews_no_translations": True
    }

    r = requests.get(url, params=params).json()

    if "result" not in r or "reviews" not in r["result"]:
        return []

    return [
        review.get("text", "")
        for review in r["result"]["reviews"]
        if review.get("text")
    ]

rows = []
for _, row in apartments.iterrows():
    print("Fetching:", row["apartment"])
    texts = fetch_reviews(row["place_id"])

    for t in texts:
        rows.append({
            "apartment": row["apartment"],
            "google_text": t
        })

df = pd.DataFrame(rows)
df.to_csv("./data/google_reviews.csv", index=False)
print("Saved google_reviews.csv")
