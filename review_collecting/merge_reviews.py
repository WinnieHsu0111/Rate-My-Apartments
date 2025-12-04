import pandas as pd
import os

# Load Google reviews (always exists)
google = pd.read_csv("./data/google_reviews.csv")

# Load Reddit (may be empty)
if os.path.exists("./data/reddit_reviews.csv") and os.path.getsize("./data/reddit_reviews.csv") > 0:
    reddit = pd.read_csv("./data/reddit_reviews.csv")
else:
    print("⚠️ Reddit file empty — using empty DataFrame.")
    reddit = pd.DataFrame(columns=["apartment", "reddit_text"])


# Load Yelp SAFELY
yelp_path = "./data/yelp_reviews.csv"

if os.path.exists(yelp_path) and os.path.getsize(yelp_path) > 0:
    try:
        yelp = pd.read_csv(yelp_path)
    except Exception:
        print("⚠️ Yelp file unreadable — using empty DataFrame.")
        yelp = pd.DataFrame(columns=["apartment", "yelp_text"])
else:
    print("⚠️ Yelp file empty — skipping Yelp.")
    yelp = pd.DataFrame(columns=["apartment", "yelp_text"])


# Merge all data
df = (
    google
    .merge(yelp, on="apartment", how="left")
    .merge(reddit, on="apartment", how="left")
)

# Save
df.to_csv("./data/all_reviews.csv", index=False)
print("\nSaved all_reviews.csv ✓")
