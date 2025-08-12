import streamlit as st
from transformers import pipeline
import os

# Suppress unnecessary warnings
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

@st.cache_resource
def load_model():
    try:
        return pipeline("summarization", model="facebook/bart-large-cnn")
    except Exception as e:
        st.error(f"Model loading failed: {str(e)}")
        return None

def summarize_text(text):
    if not text.strip():
        return []
    
    summarizer = load_model()
    if summarizer is None:
        return []
    
    try:
        summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
        points = summary[0]['summary_text'].split('. ')
        return [f"{i+1}. {point.strip()}." for i, point in enumerate(points) if point.strip()][:5]
    except Exception as e:
        st.error(f"Summarization failed: {str(e)}")
        return []

# App UI
st.set_page_config(page_title="Text Summarizer", layout="wide")
st.title("📝 Text Summarizer Tool")

# Input area
with st.container():
    user_input = st.text_area(
        "Paste your text here (min. 50 characters for best results):",
        height=200,
        placeholder="e.g., news articles, research papers, long emails..."
    )

# Summarize button
if st.button("Summarize", type="primary"):
    if len(user_input) < 50:
        st.warning("Please enter at least 50 characters for a meaningful summary.")
    else:
        with st.spinner("Generating summary..."):
            summary_points = summarize_text(user_input)
            
            if summary_points:
                st.success("Summary generated!")
                st.divider()
                st.subheader("Key Points:")
                for point in summary_points:
                    st.markdown(f"- {point}")
            else:
                st.error("Failed to generate summary. Please try again.")