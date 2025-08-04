import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configure app
st.set_page_config(page_title="Quotes Explorer", layout="wide")
st.title("📜 Quotes Analysis Dashboard")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv('quotes_data.csv')

df = load_data()

# Show raw data
st.header("All Quotes")
st.dataframe(df, height=300)

# Search functionality
st.header("🔍 Search Quotes")
search_term = st.text_input("Enter keywords:")
if search_term:
    results = df[df['quote'].str.contains(search_term, case=False)]
    st.dataframe(results)

# Analysis section
st.header("📊 Insights")

# Top authors chart
st.subheader("Most Prolific Authors")
top_authors = df['author'].value_counts().head(10)
st.bar_chart(top_authors)

# Word frequency
st.subheader("Most Common Words")
all_words = ' '.join(df['quote']).lower()
words = pd.Series(all_words.split())
meaningful_words = words[words.str.len() > 3]  # Ignore short words
word_counts = meaningful_words.value_counts().head(15)
st.bar_chart(word_counts)

# Statistics
st.subheader("Statistics")
col1, col2 = st.columns(2)
col1.metric("Total Quotes", len(df))
col2.metric("Unique Authors", df['author'].nunique())