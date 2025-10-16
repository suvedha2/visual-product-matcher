import json
import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import numpy as np
import os

# --- Configuration ---
MODEL_NAME = "openai/clip-vit-base-patch32"
PRODUCT_JSON_PATH = "products.json"
IMAGE_FOLDER_PATH = "images/"
OUTPUT_EMBEDDINGS_PATH = "product_embeddings.npy"
OUTPUT_IDS_PATH = "product_ids.json"

# --- Load Model ---
print("Loading CLIP model... (This might take a moment on first run)")
device = "cuda" if torch.cuda.is_available() else "cpu"
model = CLIPModel.from_pretrained(MODEL_NAME).to(device)
processor = CLIPProcessor.from_pretrained(MODEL_NAME)
print("✅ Model loaded.")

# --- Load Product Data ---
with open(PRODUCT_JSON_PATH, 'r') as f:
    products = json.load(f)

# --- Process Images and Generate Embeddings ---
all_embeddings = []
all_product_ids = []

print(f"Processing {len(products)} images...")
for product in products:
    try:
        image_path = os.path.join(IMAGE_FOLDER_PATH, product["image_url"])
        image = Image.open(image_path).convert("RGB") # Convert to RGB for consistency
        
        inputs = processor(text=None, images=image, return_tensors="pt", padding=True).to(device)
        image_features = model.get_image_features(**inputs)
        
        # Normalize the features to get the final embedding
        embedding = image_features[0].cpu().detach().numpy()
        embedding = embedding / np.linalg.norm(embedding)
        
        all_embeddings.append(embedding)
        all_product_ids.append(product["id"])
        print(f"  Processed: {product['name']}")

    except Exception as e:
        print(f"❌ Could not process {product['name']}. Error: {e}")

# --- Save Embeddings and IDs ---
np.save(OUTPUT_EMBEDDINGS_PATH, np.array(all_embeddings))
with open(OUTPUT_IDS_PATH, 'w') as f:
    json.dump(all_product_ids, f)

print("\n✨ Indexing complete!")
print(f"Embeddings saved to -> {OUTPUT_EMBEDDINGS_PATH}")
print(f"Product IDs saved to -> {OUTPUT_IDS_PATH}")