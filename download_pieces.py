import os
import requests
from pathlib import Path
from PIL import Image
from cairosvg import svg2png
from io import BytesIO

# Create assets directory if it doesn't exist
ASSETS_DIR = Path('assets')
ASSETS_DIR.mkdir(exist_ok=True)

# Chess piece SVG URLs (using lichess pieces)
PIECES = {
    'pawn': 'https://raw.githubusercontent.com/lichess-org/lila/master/public/piece/cburnett/wP.svg',
    'rook': 'https://raw.githubusercontent.com/lichess-org/lila/master/public/piece/cburnett/wR.svg',
    'knight': 'https://raw.githubusercontent.com/lichess-org/lila/master/public/piece/cburnett/wN.svg',
    'bishop': 'https://raw.githubusercontent.com/lichess-org/lila/master/public/piece/cburnett/wB.svg',
    'queen': 'https://raw.githubusercontent.com/lichess-org/lila/master/public/piece/cburnett/wQ.svg',
    'king': 'https://raw.githubusercontent.com/lichess-org/lila/master/public/piece/cburnett/wK.svg'
}

def download_and_convert_piece(url, size=128):
    """Download SVG from URL and convert to PNG"""
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to download from {url}")
    
    # Convert SVG to PNG using cairosvg
    png_data = svg2png(bytestring=response.content, output_width=size, output_height=size)
    return Image.open(BytesIO(png_data))

def create_colored_piece(img, color):
    """Create a colored version of the piece"""
    # Create a new image with the desired color
    colored = Image.new('RGBA', img.size, color + (0,))  # Transparent background
    
    # Use the original image as a mask
    colored.putalpha(img.getchannel('A'))
    return colored

def create_pieces():
    for piece, url in PIECES.items():
        print(f"Creating {piece}...")
        try:
            # Download and convert the SVG
            piece_img = download_and_convert_piece(url)
            
            # Create red version
            red_img = create_colored_piece(piece_img, (255, 0, 0))
            red_img.save(ASSETS_DIR / f"{piece}_red.png")
            
            # Create blue version
            blue_img = create_colored_piece(piece_img, (0, 0, 255))
            blue_img.save(ASSETS_DIR / f"{piece}_blue.png")
            
        except Exception as e:
            print(f"Error creating {piece}: {str(e)}")
            continue
    
    print("Done! Chess pieces have been created.")


def create_pieces():
    for piece in PIECES.keys():
        print(f"Creating {piece}...")
        
        # Create red version
        red_img = draw_piece(piece, 'red')
        red_img.save(ASSETS_DIR / f"{piece}_red.png")
        
        # Create blue version
        blue_img = draw_piece(piece, 'blue')
        blue_img.save(ASSETS_DIR / f"{piece}_blue.png")
        
    print("Done! Chess pieces have been created.")

if __name__ == '__main__':
    create_pieces()
