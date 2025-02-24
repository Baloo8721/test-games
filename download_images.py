import os
import requests
from pathlib import Path

# Create images directory if it doesn't exist
IMAGE_DIR = Path('images')
IMAGE_DIR.mkdir(exist_ok=True)

# Function to download and save an image
def download_image(url, filename):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(IMAGE_DIR / filename, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded {filename}")
        else:
            print(f"Failed to download {filename}")
    except Exception as e:
        print(f"Error downloading {filename}: {e}")

# Example meme images (replace with actual meme URLs)
images = {
    # Red team
    'trump_meme.jpg': 'https://example.com/trump_meme.jpg',
    'mtg_meme.jpg': 'https://example.com/mtg_meme.jpg',
    # Add more image URLs here
}

# Download all images
for filename, url in images.items():
    download_image(url, filename)
