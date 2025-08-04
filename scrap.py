import streamlit as st
import pandas as pd
from collections import Counter

def main():
    # Configure page settings first
    st.set_page_config(
        page_title="Quotes Explorer",
        page_icon="📜",
        layout="wide"
    )
    
    # App title and description
    st.title("📜 Quotes Explorer")
    st.markdown("Explore and analyze famous quotes from various authors")
    
    try:
        # Load data with error handling
        @st.cache_data
        def load_data():
            return pd.read_csv('Quotes Dataset.csv')
        
        df = load_data()
        
        # Data preview section
        with st.expander("🔍 View Raw Data", expanded=False):
            st.dataframe(df, use_container_width=True)
        
        # Search functionality
        st.subheader("Search Quotes")
        search_term = st.text_input("Enter keywords:")
        
        if search_term:
            search_results = df[df['Quote'].str.contains(search_term, case=False, na=False)]
            if not search_results.empty:
                st.success(f"Found {len(search_results)} matching quotes")
                st.dataframe(search_results, use_container_width=True)
            else:
                st.warning("No quotes found matching your search")
        
        # Analysis section
        st.subheader("📊 Analysis")
        
        # Top authors
        st.markdown("### Top 10 Most Quoted Authors")
        top_authors = df['Author'].value_counts().head(10)
        st.bar_chart(top_authors)
        
        # Word frequency
        st.markdown("### Most Common Words (excluding short/common words)")
        
        # Process words
        all_words = ' '.join(df['Quote'].astype(str)).lower().split()
        stopwords = {'the', 'and', 'to', 'of', 'a', 'in', 'is', 'it', 'that', 'for', 
                    'you', 'be', 'with', 'on', 'not', 'as', 'are', 'this', 'but', 'have'}
        meaningful_words = [word for word in all_words if word not in stopwords and len(word) > 3]
        
        # Display word cloud
        word_counts = Counter(meaningful_words).most_common(20)
        word_df = pd.DataFrame(word_counts, columns=['Word', 'Count'])
        
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(word_df, use_container_width=True)
        with col2:
            st.write("")  # Placeholder for visualization
        
        # Statistics
        st.markdown("### Dataset Statistics")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Quotes", len(df))
        col2.metric("Unique Authors", df['Author'].nunique())
        col3.metric("Avg Quote Length", f"{round(df['Quote'].str.len().mean())} chars")
        
    except FileNotFoundError:
        st.error("Error: 'Quotes Dataset.csv' not found in the current directory")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()