import os
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ----------------------------------------------------
# TEXT CLEANING + LENGTH CONTROL
# ----------------------------------------------------
def clean_text(text, max_chars=12000):
    """
    Ensures text is not too long for the model.
    Keeps first and last parts to preserve context.
    """
    if not isinstance(text, str):
        return ""

    text = text.strip()

    if len(text) <= max_chars:
        return text

    # Keep the first & last chunks
    head = text[:6000]
    tail = text[-6000:]
    return head + "\n...\n" + tail


def merge_reviews(group):
    """
    Remove duplicate lines, merge all text safely.
    """
    merged = " ".join(set(group.dropna()))
    return clean_text(merged)


# ----------------------------------------------------
# MAIN SUMMARIZER (FINAL VERSION)
# ----------------------------------------------------
def summarize_apartment(text):
    """
    Summarize apartment reviews into clear bullet points across categories.
    """

    cleaned = clean_text(text)

    prompt = f"""
Summarize the apartment review text below into clear, concise BULLET POINTS under the following categories:

- Location
- Management
- Noise
- Safety
- Unit Quality
- Price/Value

Rules:
- Use bullet points only (no paragraph).
- Only include information supported by the text.
- If a category has no evidence, write “No information provided.”
- Keep bullets short and factual.
- No assumptions.

TEXT:
{cleaned}
"""

    try:
        resp = client.responses.create(
            model="gpt-4.1",
            input=prompt
        )
        return resp.output_text.strip()

    except Exception as e:
        print("LLM summary error:", e)
        return "Summary unavailable."



# ----------------------------------------------------
# SENTIMENT CLASSIFIER (FAST + ROBUST)
# ----------------------------------------------------
def classify_sentiment(summary):
    """
    Returns (label, score).
    Score: positive=1, neutral=0, negative=-1.
    """

    prompt = f"""
Classify the following apartment summary as Positive, Neutral, or Negative.
Answer only with the label.

SUMMARY:
{summary}
"""

    try:
        resp = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )

        output = resp.output_text.lower()

    except Exception as e:
        print("Sentiment error:", e)
        return "unknown", None

    if "positive" in output:
        return "positive", 1
    if "negative" in output:
        return "negative", -1
    return "neutral", 0


# ----------------------------------------------------
# PROCESS ALL APARTMENTS
# ----------------------------------------------------
def process_all_reviews(input_csv="./data/all_reviews.csv",
                        output_csv="./data/final_summaries.csv"):

    print("🔍 Loading merged review dataset...")
    df = pd.read_csv(input_csv)

    # Combine Google + Reddit reviews safely
    df["merged_text"] = df[["google_text", "reddit_text"]].fillna("").agg(" ".join, axis=1)

    # Remove duplicate repeated text
    grouped = (
        df.groupby("apartment")["merged_text"]
        .apply(merge_reviews)
        .reset_index()
    )

    summaries = []
    sentiments = []
    sentiment_scores = []

    print(f"🏠 Processing {len(grouped)} apartments...\n")

    for i, row in grouped.iterrows():
        apt = row["apartment"]
        text = row["merged_text"]

        print(f"🏠 Summarizing: {apt}")

        summary = summarize_apartment(text)
        senti_label, senti_score = classify_sentiment(summary)

        summaries.append(summary)
        sentiments.append(senti_label)
        sentiment_scores.append(senti_score)

        print(f"   → Sentiment: {senti_label}")

    grouped["summary"] = summaries
    grouped["sentiment"] = sentiments
    grouped["sentiment_score"] = sentiment_scores

    grouped.to_csv(output_csv, index=False)

    print(f"\n💾 Saved final summaries → {output_csv}")


# ----------------------------------------------------
# RUN
# ----------------------------------------------------
if __name__ == "__main__":
    process_all_reviews()
