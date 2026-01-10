import requests
from PIL import Image
from transformers import AutoProcessor, BlipForConditionalGeneration

# Load the pretrained processor and model
processor = AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Load your image, DON'T FORGET TO WRITE YOUR IMAGE NAME
img_path = "room.jpeg"
# convert it into an RGB format 
image = Image.open(img_path).convert('RGB')

# You do not need a question for image captioning
text = ""
inputs = processor(images=image, return_tensors="pt")

# Generate a caption for the image
outputs = model.generate(**inputs, max_length=5000)

print(outputs)

# Decode the generated tokens to text
caption = processor.decode(outputs[0], skip_special_tokens=True)
# Print the caption
print(caption)