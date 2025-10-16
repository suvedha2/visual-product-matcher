import json
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel
import numpy as np
from scipy.spatial.distance import cosine
import io

# --- 1. SETUP & MODEL LOADING ---
app = FastAPI()

# Mount the 'images' directory to serve product images
app.mount("/images", StaticFiles(directory="images"), name="images")

# Load the CLIP model and processor
print("Loading CLIP model...")
device = "cuda" if torch.cuda.is_available() else "cpu"
MODEL_NAME = "openai/clip-vit-base-patch32"
model = CLIPModel.from_pretrained(MODEL_NAME).to(device)
processor = CLIPProcessor.from_pretrained(MODEL_NAME)
print("✅ Model loaded.")

# Load the pre-computed product data and embeddings
product_data = json.load(open("products.json"))
product_embeddings = np.load("product_embeddings.npy")
product_ids = json.load(open("product_ids.json"))

# Create a quick lookup map for product data by ID
product_id_map = {p["id"]: p for p in product_data}

# --- 2. CORS MIDDLEWARE ---
# This allows your frontend (running on a different port) to communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# --- 3. API ENDPOINT ---
@app.post("/api/search")
async def search(image: UploadFile = File(...)):
    # Read the uploaded image file
    contents = await image.read()
    uploaded_image = Image.open(io.BytesIO(contents)).convert("RGB")

    # Process the image and generate its embedding
    inputs = processor(text=None, images=uploaded_image, return_tensors="pt", padding=True).to(device)
    image_features = model.get_image_features(**inputs)
    query_embedding = image_features[0].cpu().detach().numpy()
    query_embedding /= np.linalg.norm(query_embedding) # Normalize

    # Calculate similarities between the query and all product images
    similarities = [1 - cosine(query_embedding, emb) for emb in product_embeddings]

    # Get the top 5 most similar products
    top_indices = np.argsort(similarities)[-5:][::-1]

    # Format the results to send back to the frontend
    results = []
    for i in top_indices:
        product_id = product_ids[i]
        product_info = product_id_map.get(product_id)
        if product_info:
            results.append({
                "product": product_info,
                "score": float(similarities[i])
            })

    return results

@app.get("/")
def read_root():
    return {"status": "Visual Product Matcher API is running"}