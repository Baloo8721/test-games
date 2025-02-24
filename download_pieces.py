import os
import requests
from pathlib import Path
from PIL import Image
import numpy as np

# Create assets directory if it doesn't exist
ASSETS_DIR = Path('assets')
ASSETS_DIR.mkdir(exist_ok=True)

# Chess piece PNG URLs (using Wikimedia Commons pieces)
PIECES = {
    'pawn': 'https://raw.githubusercontent.com/lichess-org/lila/master/public/piece/cburnett/wP.svg',
    'rook': 'https://raw.githubusercontent.com/lichess-org/lila/master/public/piece/cburnett/wR.svg',
    'knight': 'https://raw.githubusercontent.com/lichess-org/lila/master/public/piece/cburnett/wN.svg',
    'bishop': 'https://raw.githubusercontent.com/lichess-org/lila/master/public/piece/cburnett/wB.svg',
    'queen': 'https://raw.githubusercontent.com/lichess-org/lila/master/public/piece/cburnett/wQ.svg',
    'king': 'https://raw.githubusercontent.com/lichess-org/lila/master/public/piece/cburnett/wK.svg'
}

def create_piece_image(size=128):
    """Create a blank piece image of the specified size"""
    return Image.new('RGBA', (size, size), (0, 0, 0, 0))

def draw_piece(piece_type, color):
    """Draw a chess piece with the specified color"""
    size = 128  # Size of the piece image
    img = create_piece_image(size)
    
    # Draw the basic shape
    if piece_type == 'pawn':
        # Simple pawn shape
        points = [(64, 100), (44, 90), (44, 60), (64, 40), (84, 60), (84, 90)]
        color_rgb = (255, 0, 0) if color == 'red' else (0, 0, 255)
        img_array = np.array(img)
        
        # Draw filled polygon
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        draw.polygon(points, fill=color_rgb + (255,))
        
    elif piece_type == 'rook':
        # Simple rook shape
        points = [(40, 100), (88, 100), (88, 80), (78, 80), (78, 40), (88, 40), (88, 30), (40, 30), (40, 40), (50, 40), (50, 80), (40, 80)]
        color_rgb = (255, 0, 0) if color == 'red' else (0, 0, 255)
        
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        draw.polygon(points, fill=color_rgb + (255,))
        
    # Add more piece types here...
    
    return img

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
