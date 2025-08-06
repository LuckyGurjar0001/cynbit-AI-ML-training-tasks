# sentiment_app.py
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import streamlit as st
import matplotlib.pyplot as plt

# --- Scrape NDTV Headlines ---
def fetch_ndtv_headlines():
    url = 'https://www.ndtv.com/latest'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    headlines = []

    for tag in soup.find_all(['h2', 'h3']):
        text = tag.get_text(strip=True)
        if len(text) > 10 and text not in headlines:
            headlines.append(text)
        if len(headlines) >= 50:
            break

    return headlines

# --- Sentiment Analysis ---
def analyze_sentiment(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"

# --- Streamlit App ---
def main():
    st.set_page_config(page_title="News Sentiment Analyzer", layout="wide")
    st.title("📰 Sentiment Analyzer for NDTV News Headlines")
    st.markdown("Scraped from [NDTV News](https://www.ndtv.com/latest)")

    with st.spinner("Fetching headlines..."):
        headlines = fetch_ndtv_headlines()

    # Analyze each headline
    sentiment_data = []
    for headline in headlines:
        sentiment = analyze_sentiment(headline)
        sentiment_data.append({'headline': headline, 'sentiment': sentiment})

    # Sidebar filter
    st.sidebar.header("📌 Filter by Sentiment")
    selected_sentiment = st.sidebar.radio(
        "Choose sentiment type:",
        ["All", "Positive", "Negative", "Neutral"]
    )

    # Filtered data
    if selected_sentiment == "All":
        filtered_data = sentiment_data
    else:
        filtered_data = [item for item in sentiment_data if item['sentiment'] == selected_sentiment]

    # Display headlines
    st.subheader(f"🗞 Showing {selected_sentiment} Headlines ({len(filtered_data)})")
    for item in filtered_data:
        st.markdown(f"🔹 **{item['sentiment']}** — {item['headline']}")

    # Count sentiment for filtered data
    sentiments = [item['sentiment'] for item in filtered_data]
    sentiment_counts = {
        "Positive": sentiments.count("Positive"),
        "Negative": sentiments.count("Negative"),
        "Neutral": sentiments.count("Neutral")
    }

    # Display bar chart
    st.subheader("📊 Sentiment Distribution (Based on Filter)")
    fig, ax = plt.subplots()
    ax.bar(sentiment_counts.keys(), sentiment_counts.values(), color=['green', 'red', 'gray'])
    ax.set_xlabel("Sentiment")
    ax.set_ylabel("Number of Headlines")
    ax.set_title(f"{selected_sentiment} Sentiment Distribution")
    st.pyplot(fig)

if __name__ == "__main__":
    main()
