# 🏠 Rate My Apartments

An AI-powered apartment review aggregation and summarization platform that collects reviews from multiple sources (Google, Reddit, Yelp) and uses OpenAI's GPT models to generate clear, concise summaries and sentiment analysis.

## Overview

This project automates the process of:
- **Collecting** apartment reviews from Google Places, Reddit, and Yelp
- **Merging** reviews from multiple sources into unified datasets
- **Summarizing** reviews into organized bullet points using GPT-4
- **Analyzing sentiment** for each apartment (positive, neutral, negative)
- **Visualizing** results in an interactive Streamlit dashboard

## Features

✨ **Multi-Source Review Collection**
- Google Places API integration
- Reddit search API integration
- Yelp API support
- Automatic deduplication and merging

🤖 **AI-Powered Summarization**
- Uses OpenAI GPT-4 to generate structured summaries
- Organizes insights by category:
  - Location
  - Management
  - Noise
  - Safety
  - Unit Quality
  - Price/Value

💭 **Sentiment Classification**
- Automatic sentiment analysis (positive, neutral, negative)
- Sentiment scoring system
- Quick classification using GPT-4 Mini

📊 **Interactive Dashboard**
- Built with Streamlit
- Browse apartments by name
- View AI-generated summaries
- Check sentiment ratings
- Explore raw review text

## Project Structure

```
Rate My Apartments/
├── app.py
├── sum_pipeline.py
├── cleaned_unified_reviews.py
├── README.md
├── .env
│
├── data/
│   ├── all_reviews.csv
│   ├── final_summaries.csv
│   ├── google_apartments.csv
│   ├── google_reviews.csv
│   ├── yelp_reviews.csv
│   ├── reddit_reviews.csv
│   └── apartment_summary.csv
│
├── review_collecting/
│   ├── get_google_apartments.py
│   ├── google_reviews.py
│   ├── yelp_reviews.py
│   ├── reddit_reviews.py
│   └── merge_reviews.py
│
└── __pycache__/

```

## Setup

### Prerequisites

- Python 3.8+
- OpenAI API key
- Google Places API key
- Streamlit

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd "Rate My Apartments"
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the project root:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   GOOGLE_API_KEY=your_google_places_api_key_here
   ```

## Usage

### Step 1: Collect Apartment Data

Fetch a list of apartments from Google Places:
```bash
python review_collecting/get_google_apartments.py
```
Output: `data/apartments_master.csv`

### Step 2: Collect Reviews

Gather reviews from all sources:

**Google Reviews:**
```bash
python review_collecting/google_reviews.py
```

**Reddit Reviews:**
```bash
python review_collecting/reddit_reviews.py
```

**Yelp Reviews:**
```bash
python review_collecting/yelp_reviews.py
```

### Step 3: Merge Reviews

Combine all reviews into a single dataset:
```bash
python review_collecting/merge_reviews.py
```
Output: `data/all_reviews.csv`

### Step 4: Generate Summaries & Sentiment

Run the main summarization pipeline:
```bash
python sum_pipeline.py
```

This script will:
- Process each apartment's merged reviews
- Generate categorized summaries using GPT-4
- Classify sentiment using GPT-4 Mini
- Save results to `data/final_summaries.csv`

### Step 5: View Interactive Dashboard

Launch the Streamlit app:
```bash
streamlit run app.py
```

Visit `http://localhost:8501` in your browser to explore apartment summaries interactively.

## Data Flow

```
Google Places API  →  Google Reviews CSV
Reddit API         →  Reddit Reviews CSV
Yelp API           →  Yelp Reviews CSV
                        ↓
                    merge_reviews.py
                        ↓
                    all_reviews.csv
                        ↓
                    sum_pipeline.py
                        ↓
                    final_summaries.csv
                        ↓
                    Streamlit Dashboard
```

## Configuration

### Summarization Options

In `sum_pipeline.py`, you can customize:

- **Max character length** for review merging (default: 12000 chars)
- **Summary categories** - Edit the `summarize_apartment()` function prompt
- **Model selection** - Change `model="gpt-4"` to other models as needed

### Text Cleaning

The pipeline includes:
- Automatic duplicate removal
- Text truncation for long reviews
- Whitespace normalization
- Safe null/NaN handling

## API Keys & Costs

### OpenAI
- **Summarization**: Uses GPT-4 (higher cost)
- **Sentiment**: Uses GPT-4 Mini (lower cost)
- Estimate: ~$0.01-0.05 per apartment depending on review volume

### Google Places
- 25 free requests per day
- Additional usage billed per request
- Highly efficient for bulk data collection

### Reddit
- Free public API (rate-limited)
- No API key required

### Yelp
- Free API tier available
- Rate limits apply

## Output Format

### final_summaries.csv

| Column | Description |
|--------|-------------|
| apartment | Apartment name |
| merged_text | Combined review text from all sources |
| summary | AI-generated structured summary |
| sentiment | Classification (positive/neutral/negative) |
| sentiment_score | Score (-1 to 1) |

### Summary Structure

```
- Location
  - bullet points about location

- Management
  - bullet points about property management

- Noise
  - bullet points about noise levels

- Safety
  - bullet points about safety

- Unit Quality
  - bullet points about unit condition/amenities

- Price/Value
  - bullet points about rent and value
```

## Troubleshooting

**Issue: "API key not found"**
- Ensure `.env` file exists with `OPENAI_API_KEY` and `GOOGLE_API_KEY`
- Check that keys are valid and have appropriate permissions

**Issue: "Summary unavailable"**
- May occur if review text is empty or too short
- Check `all_reviews.csv` to verify merged_text is populated

**Issue: Empty CSV files after collection**
- Verify API keys are working
- Check rate limits (especially for Reddit/Google)
- Ensure search terms match actual apartments

**Issue: Streamlit connection errors**
- Make sure `final_summaries.csv` exists and is properly formatted
- Try deleting the cache: `rm -rf ~/.streamlit/`

## Limitations & Future Improvements

### Current Limitations
- Google Places API has usage limits
- LLM summaries depend on quality of source reviews
- Sentiment classification is simplified (3 categories)
- No support for review photos/images

### Future Enhancements
- [ ] Add more review sources (Apartment.com, Zillow, etc.)
- [ ] Implement caching to reduce API calls
- [ ] Add time-series analysis (review trends over time)
- [ ] Develop rating system beyond sentiment
- [ ] Add filtering/sorting by category
- [ ] Implement user accounts and favorites
- [ ] Add comparison views for multiple apartments

