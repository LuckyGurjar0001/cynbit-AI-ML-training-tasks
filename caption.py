from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import os

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base",
    use_safetensors=True,
    trust_remote_code=True
)

# Function to generate captions
def generate_caption(image_path):
    image = Image.open(image_path).convert('RGB')  # Load image
    inputs = processor(images=image, return_tensors="pt")  
    output = model.generate(**inputs)  # Get model prediction
    caption = processor.decode(output[0], skip_special_tokens=True)  # Convert to text
    return caption

image_folder = "sample_images"  
os.makedirs(image_folder, exist_ok=True) 

image_files = [
    os.path.join(image_folder, img)
    for img in os.listdir(image_folder)
    if img.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
]

# Generate and print the caption
for img_path in image_files:
    caption = generate_caption(img_path)
    print(f"Image: {img_path} -> Caption: {caption}")
