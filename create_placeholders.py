import pygame
from pathlib import Path

# Initialize Pygame
pygame.init()

# Create images directory if it doesn't exist
IMAGE_DIR = Path('images')
IMAGE_DIR.mkdir(exist_ok=True)

# Function to create a placeholder image
def create_placeholder(filename, text, color):
    surface = pygame.Surface((200, 200))
    surface.fill((255, 255, 255))  # White background
    
    # Draw colored rectangle
    pygame.draw.rect(surface, color, (10, 10, 180, 180))
    
    # Add text
    font = pygame.font.SysFont('Arial', 24)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(100, 100))
    surface.blit(text_surface, text_rect)
    
    # Save the image
    pygame.image.save(surface, IMAGE_DIR / filename)
    print(f"Created {filename}")

# Create placeholder images for all pieces
pieces = {
    # Red team
    'trump': ('Donald Trump', (200, 50, 50)),
    'mtg': ('MTG', (200, 50, 50)),
    'vivek': ('Vivek', (200, 50, 50)),
    'cruz': ('Cruz', (200, 50, 50)),
    'elon': ('Elon', (200, 50, 50)),
    'desantis': ('DeSantis', (200, 50, 50)),
    'rand': ('Rand', (200, 50, 50)),
    'pence': ('Pence', (200, 50, 50)),
    'gaetz': ('Gaetz', (200, 50, 50)),
    'mccarthy': ('McCarthy', (200, 50, 50)),
    'greene': ('Greene', (200, 50, 50)),
    'hawley': ('Hawley', (200, 50, 50)),
    'jordan': ('Jordan', (200, 50, 50)),
    'boebert': ('Boebert', (200, 50, 50)),
    'abbott': ('Abbott', (200, 50, 50)),
    'scott': ('Scott', (200, 50, 50)),
    
    # Blue team
    'biden': ('Biden', (50, 50, 200)),
    'harris': ('Harris', (50, 50, 200)),
    'pelosi': ('Pelosi', (50, 50, 200)),
    'schumer': ('Schumer', (50, 50, 200)),
    'aoc': ('AOC', (50, 50, 200)),
    'bernie': ('Bernie', (50, 50, 200)),
    'warren': ('Warren', (50, 50, 200)),
    'pete': ('Pete', (50, 50, 200)),
    'trudeau': ('Trudeau', (50, 50, 200)),
    'newsom': ('Newsom', (50, 50, 200)),
    'obama': ('Obama', (50, 50, 200)),
    'clinton': ('Clinton', (50, 50, 200)),
    'waters': ('Waters', (50, 50, 200)),
    'omar': ('Omar', (50, 50, 200)),
    'fetterman': ('Fetterman', (50, 50, 200)),
    'whitmer': ('Whitmer', (50, 50, 200)),
}

# Create portrait and meme images for each piece
for name, (text, color) in pieces.items():
    create_placeholder(f"{name}.jpg", f"{text}\nPortrait", color)
    create_placeholder(f"{name}_meme.jpg", f"{text}\nMeme!", color)

# Create golden chainsaw trophy
create_placeholder("golden_chainsaw.jpg", "Trophy!", (255, 215, 0))  # Gold color

print("All placeholder images created!")
