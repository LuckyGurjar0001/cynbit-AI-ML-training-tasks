import streamlit as st
import joblib
import numpy as np

# 1. Load model
model = joblib.load('emotion_model.pkl')
classes = model.classes_

# 2. Emoji Mapping
emotion_emoji = {
    'joy': '😄',
    'anger': '😡',
    'sadness': '😢',
    'fear': '😨',
    'love': '❤️',
    'surprise': '😲',
    'cool face':'😎',
    'sleeping':'😴',
    'disgust':'😝',
    'excitement':'😃',
    'celebration':'🙌',
    'relief':'😌',
    'eyes':'👀'
}

# 3. Streamlit UI
st.title("🧠 Emotion Detector App")
st.write("Enter a sentence to detect the emotion:")

user_input = st.text_input("Your text here:")
if st.button("Detect Emotion"):
    if user_input.strip() == "":
        st.warning("⚠️ Please enter some text!")
    else:
        pred = model.predict([user_input])[0]
        prob = model.predict_proba([user_input])[0]

        # Display result
        st.markdown(f"### Predicted Emotion: {pred} {emotion_emoji.get(pred, '')}")

        # Show probability chart
        st.bar_chart({cls: prob[i] for i, cls in enumerate(classes)})
        # sidebar 
        st.sidebar.title(" # check your emojies:")
        st.checkbox(" ✅ emoj ")
        st.sidebar.text_input("enter your expressions")
        st.sidebar.button("submit emoji")
        st.sidebar.radio("choose your emojies",['😄',  '😡', '😢',   '😨', '❤️',  '😲',  '😎', '😴',  '😝', '😃', '🙌', '😌', '👀'])
