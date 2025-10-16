# backend/populate_data.py
import os
import json
import shutil
import random

# --- Configuration ---
SOURCE_DATASET_FOLDER = 'apparel-images-dataset'
DEST_IMAGES_FOLDER = 'images'
OUTPUT_JSON_PATH = 'products.json'
NUM_PRODUCTS = 50

print("Starting data population script for multi-folder dataset...")

# --- 1. Find all available images in their subfolders ---
all_image_paths = []
try:
    # Get a list of the color subfolders (e.g., 'black', 'blue')
    color_folders = [d for d in os.listdir(SOURCE_DATASET_FOLDER) if os.path.isdir(os.path.join(SOURCE_DATASET_FOLDER, d))]
except FileNotFoundError:
    print(f"ERROR: Could not find the dataset folder at '{SOURCE_DATASET_FOLDER}'.")
    print("Please make sure you have downloaded and unzipped the 'apparel-images-dataset' folder into the 'backend' directory.")
    exit()

for color in color_folders:
    color_path = os.path.join(SOURCE_DATASET_FOLDER, color)
    for filename in os.listdir(color_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            # Store the full path, the color (category), and the filename
            all_image_paths.append((os.path.join(color_path, filename), color, filename))

print(f"Found {len(all_image_paths)} total images across {len(color_folders)} categories.")

# --- 2. Select a Random Sample ---
if len(all_image_paths) < NUM_PRODUCTS:
    sample_images = all_image_paths
else:
    random.seed(42) # Use a seed for consistent, repeatable random results
    sample_images = random.sample(all_image_paths, NUM_PRODUCTS)
print(f"Selected a random sample of {len(sample_images)} products.")

# --- 3. Prepare Folders ---
# Clear out any old images to start fresh
if os.path.exists(DEST_IMAGES_FOLDER):
    shutil.rmtree(DEST_IMAGES_FOLDER)
os.makedirs(DEST_IMAGES_FOLDER)

product_list = []
product_id_counter = 1

# --- 4. Copy Images and Generate JSON ---
print(f"Copying images to '{DEST_IMAGES_FOLDER}' and generating JSON...")
for source_path, color, original_filename in sample_images:
    # Create a new, unique filename to avoid conflicts (e.g., product_1.jpg)
    new_filename = f"product_{product_id_counter}{os.path.splitext(original_filename)[1]}"
    dest_path = os.path.join(DEST_IMAGES_FOLDER, new_filename)
    
    # Copy the image file from its subfolder to our main images folder
    shutil.copy(source_path, dest_path)
    
    product_name = f"{color.capitalize()} Apparel Item"

    product_entry = {
        "id": product_id_counter,
        "name": product_name,
        "category": "Apparel",
        "price": round(float(product_id_counter % 50 + 25), 2), # Create a fake price
        "description": f"A high-quality {color} apparel item.",
        "image_url": new_filename
    }
    product_list.append(product_entry)
    product_id_counter += 1

# --- 5. Save the JSON File ---
with open(OUTPUT_JSON_PATH, 'w') as f:
    json.dump(product_list, f, indent=2)

print("\n✨ Script finished!")
print(f"Successfully copied {len(product_list)} high-resolution images.")
print(f"Generated '{OUTPUT_JSON_PATH}' with {len(product_list)} products.")