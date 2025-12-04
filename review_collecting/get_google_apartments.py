import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

def get_google_apartments():
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"

    params = {
        "query": "apartments in Ann Arbor, MI",
        "key": API_KEY
    }

    all_results = []
    next_page = None

    print("Searching Google Places for apartments...")

    while True:
        if next_page:
            params["pagetoken"] = next_page

        r = requests.get(url, params=params).json()

        if "results" not in r:
            break

        for place in r["results"]:
            all_results.append({
                "apartment": place["name"],
                "place_id": place["place_id"],
                "lat": place["geometry"]["location"]["lat"],
                "lon": place["geometry"]["location"]["lng"]
            })

        next_page = r.get("next_page_token")
        if not next_page:
            break

        import time
        time.sleep(2)

    df = pd.DataFrame(all_results).drop_duplicates("apartment")
    df.to_csv("./data/apartments_master.csv", index=False)

    print(f"Saved {len(df)} apartments → data/apartments_master.csv")

if __name__ == "__main__":
    get_google_apartments()
