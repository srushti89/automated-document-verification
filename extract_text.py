import os
import io
from google.cloud import vision
from google.cloud.vision_v1 import types
from PIL import Image
import cv2

# Set up Google Cloud Vision Client
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "docverification-455320-aaaa7897a41e.json"
client = vision.ImageAnnotatorClient()

# Extract text from image
def extract_text(image_path):
    with io.open(image_path, "rb") as image_file:
        content = image_file.read()
    
    image = types.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        return texts[0].description  # Return the most confident extracted text
    return None

# Run extraction
if __name__ == "__main__":
    img_path = "data/sample_aadhaar.jpg"
    extracted_text = extract_text(img_path)
    print("Extracted Aadhaar Text:\n", extracted_text)
 
