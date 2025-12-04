import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("YELP_API_KEY")
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

apartments = pd.read_csv("./data/apartments_master.csv")

def find_business(name):
    url = "https://api.yelp.com/v3/businesses/search"
    params = {
        "term": name,
        "location": "Ann Arbor, MI",
        "limit": 3
    }
    r = requests.get(url, headers=HEADERS, params=params).json()
    if "businesses" not in r:
        return None
    return r["businesses"][0]["id"]

def fetch_reviews(business_id):
    url = f"https://api.yelp.com/v3/businesses/{business_id}/reviews"
    r = requests.get(url, headers=HEADERS).json()

    if "reviews" not in r:
        return []

    return [review["text"] for review in r["reviews"]]

rows = []
for apt in apartments["apartment"]:
    try:
        print("Searching Yelp:", apt)
        biz = find_business(apt)
        if not biz:
            continue

        texts = fetch_reviews(biz)
        for t in texts:
            rows.append({"apartment": apt, "yelp_text": t})
    except:
        continue

pd.DataFrame(rows).to_csv("./data/yelp_reviews.csv", index=False)
print("Saved yelp_reviews.csv")
