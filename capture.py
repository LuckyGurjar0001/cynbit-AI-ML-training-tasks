import cv2
from fer import FER
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def real_time_emotion_detection():
    # Initialize the emotion detector
    emotion_detector = FER(mtcnn=True)  # Using MTCNN for better face detection
    
    # Start webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return
    
    print("Emotion detection started. Press 'q' to quit.")
    
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break
        
        # Convert frame to RGB (FER uses RGB)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        try:
            # Detect emotions
            emotions = emotion_detector.detect_emotions(rgb_frame)
            
            # Process each face found
            for face in emotions:
                x, y, w, h = face["box"]
                emotions = face["emotions"]
                
                # Draw rectangle around face
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                
                # Get dominant emotion
                dominant_emotion = max(emotions.items(), key=lambda x: x[1])[0]
                
                # Display emotion text
                cv2.putText(frame, f"{dominant_emotion}: {emotions[dominant_emotion]:.2f}", 
                           (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                
                # Display all emotions (optional)
                emotion_text = ", ".join([f"{k}: {v:.2f}" for k, v in emotions.items()])
                cv2.putText(frame, emotion_text, (x, y+h+20), 
                          cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
        
        except Exception as e:
            print(f"Error in emotion detection: {e}")
        
        # Display the resulting frame
        cv2.imshow('Real-Time Emotion Detection', frame)
        
        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    real_time_emotion_detection()