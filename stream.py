import streamlit as st
from fer import FER
import cv2
from PIL import Image
import numpy as np

st.title("Real-Time Emotion Detection")

# Initialize detector
detector = FER(mtcnn=True)

# Create a button to start/stop detection
run = st.checkbox('Start Detection')

# Placeholder for the webcam feed
FRAME_WINDOW = st.image([])

# Start webcam
cap = cv2.VideoCapture(0)

while run:
    ret, frame = cap.read()
    if not ret:
        st.error("Failed to capture video")
        break
    
    # Convert to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    try:
        # Detect emotions
        emotions = detector.detect_emotions(rgb_frame)
        
        # Process each face
        for face in emotions:
            x, y, w, h = face["box"]
            emotions = face["emotions"]
            
            # Draw rectangle
            cv2.rectangle(rgb_frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            # Get dominant emotion
            dominant_emotion = max(emotions.items(), key=lambda x: x[1])[0]
            
            # Display emotion
            cv2.putText(rgb_frame, dominant_emotion, (x, y-10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    
    except Exception as e:
        st.warning(f"Detection error: {e}")
    
    # Display frame
    FRAME_WINDOW.image(rgb_frame)

else:
    st.write('Stopped')

# Release resources when done
cap.release()