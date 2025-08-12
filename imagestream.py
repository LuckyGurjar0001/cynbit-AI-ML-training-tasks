# streamlit_image_classification.py

import streamlit as st
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image

# 1. Load pre-trained model
model = MobileNetV2(weights='imagenet')

# 2. Streamlit UI
st.title("🖼️ Image Classification App")
st.write("Upload an image and let MobileNetV2 guess what it is!")

# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "webp", "png"])

if uploaded_file is not None:
    # Show uploaded image
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Image", use_column_width=True)

    # Preprocess image
    img = img.resize((224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    # Make prediction
    predictions = model.predict(img_array)
    decoded = decode_predictions(predictions, top=3)[0]  # Show top 3 predictions

    st.subheader("Predictions:")
    for i, (imagenet_id, label, score) in enumerate(decoded):
        st.write(f"{i+1}. **{label}** — {score*100:.2f}% confidence")
