
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import numpy as np
import os

# 1. Load Pre-trained Model
model = MobileNetV2(weights='imagenet')

# 2. Path to your images folder
image_folder = "images"  # Create a folder named 'images' and put 5-10 images there

# 3. Loop through each image
for img_name in os.listdir(image_folder):
    img_path = os.path.join(image_folder, img_name)

    img = image.load_img(img_path, target_size=(224, 224))
    
    img_array = image.img_to_array(img)

    img_array = np.expand_dims(img_array, axis=0)

    # Preprocess image for MobileNetV2
    img_array = preprocess_input(img_array)

    predictions = model.predict(img_array)

    # Decode predictions to human-readable labels
    decoded = decode_predictions(predictions, top=1)[0][0]
    label = decoded[1]   # Class name
    confidence = decoded[2] * 100  # Confidence score in %

    print(f"Image: {img_name}")
    print(f"Predicted: {label} ({confidence:.2f}%)\n")

