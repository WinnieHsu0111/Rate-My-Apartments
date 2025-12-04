import requests
import pandas as pd
import time

apartments = pd.read_csv("./data/apartments_master.csv")

def search_reddit(query):
    url = f"https://www.reddit.com/search.json?q={query}+Ann+Arbor&limit=50"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers).json()

    if "data" not in r or "children" not in r["data"]:
        return []

    posts = []
    for post in r["data"]["children"]:
        data = post["data"]
        posts.append({
            "title": data.get("title", ""),
            "text": data.get("selftext", ""),
        })
    return posts

rows = []
for apt in apartments["apartment"]:
    print("Searching Reddit:", apt)
    posts = search_reddit(apt)
    time.sleep(1)

    for p in posts:
        combined = (p["title"] + " " + p["text"]).strip()
        if combined:
            rows.append({"apartment": apt, "reddit_text": combined})

pd.DataFrame(rows).to_csv("./data/reddit_reviews.csv", index=False)
print("Saved reddit_reviews.csv")
