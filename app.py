import streamlit as st
import pandas as pd

# load data
@st.cache_data
def load_data():
    return pd.read_csv("./data/final_summaries.csv")

df = load_data()

st.set_page_config(page_title="Rate My Apartments – Summary Viewer", layout="centered")

st.title("🏠 Rate My Apartments – LLM Summaries")
st.write("Browse AI-generated summaries for Ann Arbor apartments based on Google + Reddit reviews.")


# apartment selection
apartments = df["apartment"].sort_values().unique()
selected = st.selectbox("Select an apartment:", apartments)

apt_row = df[df["apartment"] == selected].iloc[0]


# summary display
st.subheader(f"📌 Summary for **{selected}**")

summary_text = apt_row["summary"]

if summary_text == "Summary unavailable." or pd.isna(summary_text):
    st.warning("No summary available for this apartment.")
else:
    st.write(summary_text)


# sentiment display
sentiment = apt_row["sentiment"]
score = apt_row["sentiment_score"]

sentiment_color = {
    "positive": "🟢 Positive",
    "neutral": "🟡 Neutral",
    "negative": "🔴 Negative",
    "unknown": "⚪ Unknown"
}

st.subheader("💬 Sentiment")
st.write(f"**Sentiment:** {sentiment_color.get(sentiment, sentiment)}")
st.write(f"**Score:** {score}")


# show raw review text
with st.expander("📂 Show raw review text"):
    st.write(apt_row["merged_text"])
