import streamlit as st
from news import NewsAnalyzer

# Initialize analyzer
analyzer = NewsAnalyzer()

# Configure Streamlit page
st.set_page_config(
    page_title="Trending Topics Extractor",
    page_icon="📰",
    layout="wide"
)

# Custom CSS for better appearance
st.markdown("""
    <style>
    .main {padding: 2rem;}
    .stSelectbox, .stTextInput {margin-bottom: 1rem;}
    .stMarkdown h2 {border-bottom: 1px solid #eee; padding-bottom: 0.5rem;}
    .highlight {background-color: #ffff00; padding: 0.1em;}
    </style>
    """, unsafe_allow_html=True)

# News sources configuration
NEWS_SOURCES = {
    "BBC News": "https://www.bbc.com/news",
    "CNN": "https://edition.cnn.com",
    "The Guardian": "https://www.theguardian.com/international",
    "Reuters": "https://www.reuters.com/",
    "Al Jazeera": "https://www.aljazeera.com/"
}

def highlight_text(text, query):
    """Highlight search query in text"""
    return text.replace(query, f'<span class="highlight">{query}</span>')

def main():
    st.title("📰 Trending Topics Extractor")
    st.markdown("Discover the most talked-about topics from major news sources")
    
    # Sidebar for settings
    with st.sidebar:
        st.header("Settings")
        source_name = st.selectbox("Select News Source", list(NEWS_SOURCES.keys()))
        visualization_type = st.radio(
            "Visualization Type", 
            ["Bar Chart", "Word Cloud"],
            index=0
        )
        st.markdown("---")
        st.markdown("**Note:** This tool scrapes live data from news websites.")
    
    # Main content area
    url = NEWS_SOURCES[source_name]
    
    with st.spinner(f"Fetching latest headlines from {source_name}..."):
        headlines = analyzer.scrape_headlines(url)
    
    if not headlines:
        st.error("Failed to fetch headlines. Please try another news source.")
        return
    
    # Show raw headlines in expander
    with st.expander("📋 View Raw Headlines", expanded=False):
        st.write(f"Total headlines: {len(headlines)}")
        for i, headline in enumerate(headlines, 1):
            st.write(f"{i}. {headline}")
    
    # Process and analyze headlines
    keywords = analyzer.preprocess_text(headlines)
    top_keywords = analyzer.get_top_keywords(keywords)
    
    # Display analysis results
    st.subheader("📊 Trend Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🔍 Top 5 Keywords**")
        for word, count in top_keywords:
            st.markdown(f"- **{word.title()}**: {count} mentions")
    
    with col2:
        st.markdown(f"**📈 {visualization_type}**")
        if visualization_type == "Bar Chart":
            fig = analyzer.plot_bar_chart(top_keywords)
        else:
            fig = analyzer.generate_wordcloud(keywords)
        st.pyplot(fig)
    
    # Search functionality
    st.subheader("🔎 Search Headlines")
    search_query = st.text_input(
        "Enter a keyword to search in headlines",
        placeholder="e.g., election, economy, sports"
    ).lower()
    
    if search_query:
        results = [h for h in headlines if search_query in h.lower()]
        
        if results:
            st.success(f"Found {len(results)} matching headlines:")
            for i, result in enumerate(results, 1):
                # Highlight the search term in results
                highlighted = highlight_text(result, search_query)
                st.markdown(f"{i}. {highlighted}", unsafe_allow_html=True)
        else:
            st.warning("No headlines found matching your search.")

if __name__ == "__main__":
    main()