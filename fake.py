# app.py
import streamlit as st
import joblib
import re
import nltk
from nltk.corpus import stopwords

# Load model and vectorizer
@st.cache_resource
def load_model():
    try:
        model = joblib.load('model.joblib')
        vectorizer = joblib.load('vectorizer.joblib')
        return model, vectorizer
    except Exception as e:
        st.error(f"Model loading failed: {str(e)}")
        st.stop()

model, vectorizer = load_model()

# Text cleaning
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

# Streamlit UI
st.title("📰 News Authenticity Checker")
user_input = st.text_area("Paste news article here:", height=200)

if st.button("Check Authenticity"):
    if user_input:
        # Clean and vectorize input
        cleaned_text = clean_text(user_input)
        text_vec = vectorizer.transform([cleaned_text])
        
        # Predict
        prediction = model.predict(text_vec)[0]
        proba = model.predict_proba(text_vec)[0][prediction]
        
        # Display result
        if prediction == 1:
            st.success(f"✅ REAL NEWS (Confidence: {proba*100:.1f}%)")
        else:
            st.error(f"❌ FAKE NEWS (Confidence: {proba*100:.1f}%)")
    else:
        st.warning("Please enter some text")