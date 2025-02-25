import pygame
import sys
import os
from typing import Optional, Tuple, List, Dict
from pathlib import Path
import pygame

# Initialize Pygame and mixer
pygame.init()
pygame.mixer.init()

# Paths
# Use relative paths from the current directory
IMAGE_DIR = Path(__file__).parent / 'images'
ASSETS_DIR = Path(__file__).parent / 'assets'
AUDIO_DIR = Path(__file__).parent / 'audio'

# Create directories if they don't exist
IMAGE_DIR.mkdir(exist_ok=True)
ASSETS_DIR.mkdir(exist_ok=True)
AUDIO_DIR.mkdir(exist_ok=True)

# Background music file path
BACKGROUND_MUSIC = AUDIO_DIR / 'politcal party lofi.mp3'

# Music control constants
MUSIC_BUTTON_SIZE = 40
MUSIC_VOLUME = 0.5  # Initial volume 50%
IS_MUTED = False  # Track mute state

# Constants
LEFT_PANEL_WIDTH = 200  # Width of the left panel
MIN_WINDOW_WIDTH = 800  # Minimum window width
MIN_WINDOW_HEIGHT = 600  # Minimum window height
WINDOW_WIDTH = 1000  # Initial window width
WINDOW_HEIGHT = 800  # Initial window height

# These will be updated when window is resized
BOARD_SIZE = 0
SQUARE_SIZE = 0
PIECE_SIZE = 0
PORTRAIT_SIZE = 0
BOARD_OFFSET_X = 0
BOARD_OFFSET_Y = 0

def update_sizes(width, height):
    global BOARD_SIZE, SQUARE_SIZE, PIECE_SIZE, PORTRAIT_SIZE, BOARD_OFFSET_X, BOARD_OFFSET_Y
    # Board size is 96% of the smaller dimension (after accounting for left panel)
    usable_width = width - LEFT_PANEL_WIDTH
    BOARD_SIZE = int(min(usable_width, height) * 0.96)
    SQUARE_SIZE = BOARD_SIZE // 8
    PIECE_SIZE = int(SQUARE_SIZE * 0.92)
    PORTRAIT_SIZE = int(height * 0.2)
    # Center the board in the remaining space
    BOARD_OFFSET_X = LEFT_PANEL_WIDTH + (usable_width - BOARD_SIZE) // 2
    BOARD_OFFSET_Y = (height - BOARD_SIZE) // 2

# Initialize sizes
update_sizes(WINDOW_WIDTH, WINDOW_HEIGHT)

# Time constants
HOVER_DELAY = 500  # milliseconds before showing portrait
CAPTURE_DISPLAY_TIME = 2000  # milliseconds to show capture meme

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 50, 50)
BLUE = (50, 50, 220)
GOLD = (255, 215, 0)  # Bright gold color for winner
BOARD_LIGHT = (255, 255, 255)  # White squares
BOARD_DARK = (128, 128, 128)   # Grey squares
HIGHLIGHT = (255, 255, 0, 128)

# Paths
# Use relative paths from the current directory
IMAGE_DIR = Path(__file__).parent / 'images'
ASSETS_DIR = Path(__file__).parent / 'assets'

# Screen setup
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption('PoliticalChess')

# Political figures for pieces
RED_PIECES = {
    'king': {'name': 'Donald Trump', 'portrait': 'trump1.jpg', 'meme': 'trump_meme1.jpg'},
    'queen': {'name': 'Pam Bondi', 'portrait': 'bondi.jpg', 'meme': 'bondi_meme.jpg'},  # TODO: Add these images
    'rook': [
        {'name': 'Vivek Ramaswamy', 'portrait': 'vivek.jpg', 'meme': 'vivek_meme.jpg'},
        {'name': 'Ted Cruz', 'portrait': 'cruz.jpg', 'meme': 'cruz_meme.jpg'}
    ],
    'knight': [
        {'name': 'Elon Musk', 'portrait': 'elon.jpg', 'meme': 'elon_meme.jpg'},
        {'name': 'Ron DeSantis', 'portrait': 'desantis.jpg', 'meme': 'desantis_meme.jpg'}
    ],
    'bishop': [
        {'name': 'Rand Paul', 'portrait': 'rand.jpg', 'meme': 'rand_meme.jpg'},
        {'name': 'Kash Patel', 'portrait': 'patel.jpg', 'meme': 'patel_meme.jpg'}
    ],
    'pawn': [
        {'name': 'Matt Gaetz', 'portrait': 'gaetz.jpg', 'meme': 'gaetz_meme.jpg'},
        {'name': 'RFK Jr', 'portrait': 'RFK Jr.jpg', 'meme': 'RFK Jr_meme.jpg'},  # Fixed portrait
        {'name': 'Marjorie T Greene', 'portrait': 'greene.jpg', 'meme': 'greene_meme.jpg'},
        {'name': 'Josh Hawley', 'portrait': 'hawley.jpg', 'meme': 'hawley_meme.jpg'},
        {'name': 'Jim Jordan', 'portrait': 'jordan.jpg', 'meme': 'jordan_meme.jpg'},
        {'name': 'Lauren Boebert', 'portrait': 'boebert.jpg', 'meme': 'boebert_meme.jpg'},
        {'name': 'Greg Abbott', 'portrait': 'abbott.jpg', 'meme': 'abbott_meme.jpg'},
        {'name': 'Tim Scott', 'portrait': 'scott.jpg', 'meme': 'scott_meme.jpg'}
    ]
}

BLUE_PIECES = {
    'king': {'name': 'Barack Obama', 'portrait': 'obama.jpg', 'meme': 'obama_meme.jpg'},
    'queen': {'name': 'Kamala Harris', 'portrait': 'harris.jpg', 'meme': 'harris_meme.jpg'},
    'rook': [
        {'name': 'Nancy Pelosi', 'portrait': 'pelosi.jpg', 'meme': 'pelosi_meme.jpg'},
        {'name': 'Chuck Schumer', 'portrait': 'schumer.jpg', 'meme': 'schumer_meme.jpg'}
    ],
    'knight': [
        {'name': 'AOC', 'portrait': 'aoc.jpg', 'meme': 'aoc_meme.jpg'},
        {'name': 'Bernie Sanders', 'portrait': 'bernie.jpg', 'meme': 'bernie_meme.jpg'}
    ],
    'bishop': [
        {'name': 'Elizabeth Warren', 'portrait': 'warren.jpg', 'meme': 'warren_meme.jpg'},
        {'name': 'Pete Buttigieg', 'portrait': 'pete.jpg', 'meme': 'pete_meme.jpg'}
    ],
    'pawn': [
        {'name': 'Justin Trudeau', 'portrait': 'trudeau.jpg', 'meme': 'trudeau_meme.jpg'},
        {'name': 'Gavin Newsom', 'portrait': 'newsom.jpg', 'meme': 'newsom_meme.jpg'},
        {'name': 'Joe Biden', 'portrait': 'biden.jpg', 'meme': 'biden_meme.jpg'},
        {'name': 'Hillary Clinton', 'portrait': 'clinton.jpg', 'meme': 'clinton_meme.jpg'},
        {'name': 'Maxine Waters', 'portrait': 'waters.jpg', 'meme': 'waters_meme.jpg'},
        {'name': 'Ilhan Omar', 'portrait': 'omar.jpg', 'meme': 'omar_meme.jpg'},
        {'name': 'John Fetterman', 'portrait': 'fetterman.jpg', 'meme': 'fetterman_meme.jpg'},
        {'name': 'Gretchen Whitmer', 'portrait': 'whitmer.jpg', 'meme': 'whitmer_meme.jpg'}
    ]
}

# Piece shapes (paths for SVG-like drawing)
PIECE_SHAPES = {
    'pawn': [
        ('M', 0.4, 0.9),   # Base left
        ('L', 0.6, 0.9),   # Base right
        ('L', 0.55, 0.7),  # Stem right
        ('A', 0.5, 0.5, 0.1),  # Rounded head (arc centered at 0.5, 0.5, radius 0.1)
        ('L', 0.45, 0.7),  # Stem left
        ('Z',)             # Close path
    ],
    'rook': [
        ('M', 0.3, 0.9),   # Base left
        ('L', 0.7, 0.9),   # Base right
        ('L', 0.7, 0.6),   # Tower right
        ('L', 0.65, 0.6),  # Notch right edge
        ('L', 0.65, 0.5),  # Notch 1 bottom
        ('L', 0.55, 0.5),  # Notch 1 top
        ('L', 0.55, 0.4),  # Notch 2 bottom
        ('L', 0.45, 0.4),  # Notch 2 top
        ('L', 0.45, 0.5),  # Notch 3 bottom
        ('L', 0.35, 0.5),  # Notch 3 top
        ('L', 0.35, 0.6),  # Notch left edge
        ('L', 0.3, 0.6),   # Tower left
        ('Z',)             # Close path
    ],
    'knight': [
        ('M', 0.35, 0.9),  # Base left
        ('L', 0.65, 0.9),  # Base right
        ('L', 0.6, 0.7),   # Neck bottom right
        ('L', 0.7, 0.5),   # Mane back
        ('L', 0.65, 0.4),  # Head top
        ('L', 0.5, 0.35),  # Snout tip
        ('L', 0.45, 0.5),  # Chin
        ('L', 0.4, 0.7),   # Neck front
        ('Z',)             # Close path
    ],
    'bishop': [
        ('M', 0.35, 0.9),  # Base left
        ('L', 0.65, 0.9),  # Base right
        ('L', 0.6, 0.65),  # Stem right
        ('L', 0.55, 0.4),  # Mitre right
        ('A', 0.5, 0.3, 0.05),  # Mitre top curve (small arc)
        ('L', 0.45, 0.4),  # Mitre left
        ('L', 0.4, 0.65),  # Stem left
        ('Z',)             # Close path
    ],
    'queen': [
        ('M', 0.3, 0.9),   # Base left
        ('L', 0.7, 0.9),   # Base right
        ('L', 0.65, 0.65), # Stem right
        ('L', 0.6, 0.5),   # Body right
        ('L', 0.65, 0.35), # Crown point 1
        ('L', 0.55, 0.4),  # Crown dip 1
        ('L', 0.5, 0.3),   # Crown point 2 (center)
        ('L', 0.45, 0.4),  # Crown dip 2
        ('L', 0.35, 0.35), # Crown point 3
        ('L', 0.4, 0.5),   # Body left
        ('L', 0.35, 0.65), # Stem left
        ('Z',)             # Close path
    ],
    'king': [
        ('M', 0.3, 0.9),   # Base left
        ('L', 0.7, 0.9),   # Base right
        ('L', 0.65, 0.65), # Stem right
        ('L', 0.6, 0.45),  # Body right
        ('L', 0.55, 0.35), # Cross base right
        ('L', 0.55, 0.25), # Cross vertical right
        ('L', 0.5, 0.2),   # Cross top
        ('L', 0.45, 0.25), # Cross vertical left
        ('L', 0.45, 0.35), # Cross base left
        ('L', 0.4, 0.45),  # Body left
        ('L', 0.35, 0.65), # Stem left
        ('Z',)             # Close path
    ]
}

class ChessPiece:
    def __init__(self, piece_type: str, color: str, piece_data: dict, x: int, y: int):
        self.piece_type = piece_type
        self.color = color
        self.x = x
        self.y = y
        self.name = piece_data['name']
        self.portrait = piece_data['portrait']
        self.meme = piece_data['meme']
        self.selected = False
        self.hover_start = 0
        self.has_moved = False
        self._portrait_surface = None
        self._meme_surface = None
        self._load_images()

    def _load_images(self):
        try:
            print(f"\n=== Loading images for {self.name} ===\n")
            portrait_path = IMAGE_DIR / self.portrait
            meme_path = IMAGE_DIR / self.meme
            
            # Debug print
            print(f"Loading images for {self.name}:")
            print(f"Portrait path: {portrait_path} (exists: {portrait_path.exists()})")
            print(f"Meme path: {meme_path} (exists: {meme_path.exists()})")
            
            # Try to convert AVIF to PNG first
            if self.name in ['Elon Musk', 'Kash Patel']:
                # Convert AVIF to PNG using sips
                png_path = portrait_path.with_suffix('.png')
                os.system(f'sips -s format png "{portrait_path}" --out "{png_path}"')
                portrait_path = png_path
            
            # Check if files exist first
            if not portrait_path.exists():
                print(f"Missing portrait for {self.name}: {self.portrait} - Please add this image to the images directory")
                return
                
            if not meme_path.exists():
                print(f"Missing meme for {self.name}: {self.meme} - Please add this image to the images directory")
                # Continue anyway to show portrait
            
            # Load portrait
            try:
                print(f"Attempting to load portrait for {self.name} from {portrait_path}...")
                portrait_img = pygame.image.load(str(portrait_path))
                print(f"Portrait loaded, attempting to scale...")
                self._portrait_surface = pygame.transform.scale(portrait_img, (SQUARE_SIZE, SQUARE_SIZE))  # Exactly fill square
                print(f"Successfully loaded and scaled portrait for {self.name}")
                print(f"Portrait surface size: {self._portrait_surface.get_size()}")
            except Exception as e:
                print(f"Error loading portrait for {self.name}: {e}")
                import traceback
                traceback.print_exc()
            
            # Load meme if it exists
            if meme_path.exists():
                try:
                    print(f"Attempting to load meme for {self.name}...")
                    meme_img = pygame.image.load(str(meme_path))
                    print(f"Meme loaded, attempting to scale...")
                    self._meme_surface = pygame.transform.scale(meme_img, (PORTRAIT_SIZE, PORTRAIT_SIZE))
                    print(f"Successfully loaded and scaled meme for {self.name}")
                    print(f"Meme surface size: {self._meme_surface.get_size()}")
                except Exception as e:
                    print(f"Error loading meme for {self.name}: {e}")
                    import traceback
                    traceback.print_exc()
                
        except Exception as e:
            print(f"Error loading images for {self.name}: {e}")
            import traceback
            traceback.print_exc()

    def draw_shape(self, surface: pygame.Surface):
        # Calculate center position of the square
        center_x = self.x * SQUARE_SIZE + SQUARE_SIZE // 2
        center_y = self.y * SQUARE_SIZE + SQUARE_SIZE // 2

        # Load and cache the piece image if not already loaded
        if not hasattr(self, '_piece_surface'):
            piece_image_path = ASSETS_DIR / f"{self.piece_type}_{self.color}.png"
            try:
                piece_img = pygame.image.load(str(piece_image_path))
                # Scale to 92% of the square size for better visibility
                scale_size = int(SQUARE_SIZE * 0.92)
                self._piece_surface = pygame.transform.scale(piece_img, (scale_size, scale_size))
            except Exception as e:
                print(f"Error loading piece image {piece_image_path}: {e}")
                return

        # Draw the piece image centered in the square
        if hasattr(self, '_piece_surface'):
            # Adjust size for queen/king
            if self.piece_type in ['queen', 'king']:
                piece_size = int(PIECE_SIZE * 0.85)  # Make queen/king 85% of normal size
            else:
                piece_size = PIECE_SIZE
                
            # Scale piece to fit
            scaled_piece = pygame.transform.scale(self._piece_surface, (piece_size, piece_size))
            piece_rect = scaled_piece.get_rect(center=(center_x, center_y))
            surface.blit(scaled_piece, piece_rect)

        # Draw name below the piece with smaller, cleaner font
        name_font_size = int(SQUARE_SIZE * 0.14)  # Base font size
        font = pygame.font.SysFont('Arial', name_font_size, bold=False)
        
        # Get last name if square is too small
        display_name = self.name
        if SQUARE_SIZE < 80:  # If square is smaller than 80 pixels
            # Split name and get last part
            name_parts = self.name.split()
            if len(name_parts) > 1:
                display_name = name_parts[-1]  # Use last name only
            else:
                display_name = self.name[:6]  # Or first 6 chars if no space
        
        name_text = font.render(display_name, True, BLACK)
        
        # Make sure text fits within square
        max_width = int(SQUARE_SIZE * 0.85)  # Max width is 85% of square
        if name_text.get_width() > max_width:
            # Scale down font size to fit
            scale = max_width / name_text.get_width()
            name_font_size = max(int(name_font_size * scale), 8)
            font = pygame.font.SysFont('Arial', name_font_size, bold=False)
            name_text = font.render(display_name, True, BLACK)
        
        # Position text with more space below piece
        spacing = int(SQUARE_SIZE * 0.2)  # Space below piece
        text_rect = name_text.get_rect(center=(center_x, center_y + SQUARE_SIZE//2 - spacing))
        surface.blit(name_text, text_rect)

    def draw_portrait(self, surface: pygame.Surface):
        if self._portrait_surface:
            # Calculate square position
            square_x = self.x * SQUARE_SIZE
            square_y = self.y * SQUARE_SIZE
            
            # Scale portrait to fit square
            scaled_portrait = pygame.transform.scale(self._portrait_surface, (SQUARE_SIZE, SQUARE_SIZE))
            
            # Draw portrait
            surface.blit(scaled_portrait, (square_x, square_y))

    def draw_capture_meme(self, surface: pygame.Surface):
        if self._meme_surface:
            # Create semi-transparent overlay
            overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))  # Dark overlay for better contrast
            surface.blit(overlay, (0, 0))
            
            # Scale meme to larger size
            meme_size = min(int(BOARD_SIZE * 0.8), 800)  # 80% of board size, max 800px
            scaled_meme = pygame.transform.scale(self._meme_surface, (meme_size, meme_size))
            
            # Center meme on screen
            meme_rect = scaled_meme.get_rect(center=(BOARD_SIZE // 2, BOARD_SIZE // 2))
            surface.blit(scaled_meme, meme_rect)
            
            # Add piece name at top
            name_font_size = int(BOARD_SIZE * 0.06)
            name_font = pygame.font.SysFont('Arial', name_font_size, bold=True)
            name_text = name_font.render(self.name, True, WHITE)
            name_rect = name_text.get_rect(center=(BOARD_SIZE // 2, BOARD_SIZE // 4))
            surface.blit(name_text, name_rect)
            
            # Add click to continue text at bottom
            font_size = int(BOARD_SIZE * 0.04)
            font = pygame.font.SysFont('Arial', font_size, bold=True)
            text = font.render('Click to continue', True, WHITE)
            text_rect = text.get_rect(center=(BOARD_SIZE // 2, BOARD_SIZE - SQUARE_SIZE))
            surface.blit(text, text_rect)

    def draw(self, surface: pygame.Surface):
        # Draw the piece shape
        self.draw_shape(surface)

        # Check for hover
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # Adjust mouse position for board offset
        board_mouse_x = mouse_x - BOARD_OFFSET_X
        board_mouse_y = mouse_y - BOARD_OFFSET_Y
        
        piece_rect = pygame.Rect(self.x * SQUARE_SIZE, self.y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        
        # Only show portrait when hovering over the piece's square
        if piece_rect.collidepoint(board_mouse_x, board_mouse_y):
            if self.hover_start == 0:
                self.hover_start = pygame.time.get_ticks()
            if self._portrait_surface:  # Only draw if we have a valid image
                self.draw_portrait(surface)
        else:
            self.hover_start = 0

class ChessGame:
    def __init__(self):
        self.board: List[List[Optional[ChessPiece]]] = [[None for _ in range(8)] for _ in range(8)]
        self.selected_piece: Optional[ChessPiece] = None
        self.turn = 'red'  # red goes first
        self.game_over = False
        self.winner = None
        self.captured_piece = None
        self.capture_time = 0
        self.waiting_for_click = False
        self.captured_pieces = []  # List to track all captured pieces
        self.winner = None
        self.captured_piece: Optional[ChessPiece] = None
        self.capture_time = 0
        self.waiting_for_click = False  # Add flag to wait for click
        self.setup_board()
        self._winner_surface = None
        try:
            winner_img = pygame.image.load(str(IMAGE_DIR / 'golden_chainsaw.jpg'))
            self._winner_surface = pygame.transform.scale(winner_img, (PORTRAIT_SIZE, PORTRAIT_SIZE))
        except Exception as e:
            print(f"Error loading winner image: {e}")

    def setup_board(self):
        # Set up red pieces (top)
        piece_order = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
        for x, piece_type in enumerate(piece_order):
            if piece_type in ['queen', 'king']:
                piece_data = RED_PIECES[piece_type]
            else:
                piece_data = RED_PIECES[piece_type][0 if x < 4 else 1]
            self.board[0][x] = ChessPiece(piece_type, 'red', piece_data, x, 0)
        
        for x in range(8):
            self.board[1][x] = ChessPiece('pawn', 'red', RED_PIECES['pawn'][x], x, 1)

        # Set up blue pieces (bottom)
        for x, piece_type in enumerate(piece_order):
            if piece_type in ['queen', 'king']:
                piece_data = BLUE_PIECES[piece_type]
            else:
                piece_data = BLUE_PIECES[piece_type][0 if x < 4 else 1]
            self.board[7][x] = ChessPiece(piece_type, 'blue', piece_data, x, 7)
        
        for x in range(8):
            self.board[6][x] = ChessPiece('pawn', 'blue', BLUE_PIECES['pawn'][x], x, 6)

    def draw(self, surface: pygame.Surface):
        # Draw board
        for y in range(8):
            for x in range(8):
                color = BOARD_LIGHT if (x + y) % 2 == 0 else BOARD_DARK
                pygame.draw.rect(surface, color, 
                               (x * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

        # Draw pieces
        for row in self.board:
            for piece in row:
                if piece:
                    piece.draw(surface)

        # Draw selected piece highlight and valid moves
        if self.selected_piece:
            # Highlight selected piece with yellow glow
            x, y = self.selected_piece.x * SQUARE_SIZE, self.selected_piece.y * SQUARE_SIZE
            highlight_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            pygame.draw.rect(highlight_surface, (255, 255, 0, 80), 
                           (0, 0, SQUARE_SIZE, SQUARE_SIZE))
            surface.blit(highlight_surface, (x, y))
            
            # Show valid moves with green dots
            for move_y in range(8):
                for move_x in range(8):
                    if self.is_valid_move(self.selected_piece, move_x, move_y):
                        # Create highlight surface for valid move
                        move_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                        
                        # Draw filled circle with border for better visibility
                        radius = int(SQUARE_SIZE * 0.15)  # Slightly smaller dots
                        center = (SQUARE_SIZE // 2, SQUARE_SIZE // 2)
                        
                        # Draw green fill
                        pygame.draw.circle(move_surface, (0, 255, 0, 160), center, radius)
                        # Draw darker border
                        pygame.draw.circle(move_surface, (0, 200, 0, 200), center, radius, 2)
                        
                        surface.blit(move_surface, (move_x * SQUARE_SIZE, move_y * SQUARE_SIZE))
            
        # Draw winner announcement if game is over
        if self.game_over and self.winner:
            try:
                # Create semi-transparent overlay for entire board
                overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 180))  # Darker overlay for better contrast
                surface.blit(overlay, (0, 0))
                
                # Draw large winner text at top
                winner_font_size = min(int(BOARD_SIZE * 0.12), 96)  # Larger text, capped at 96pt
                font = pygame.font.SysFont('Arial', winner_font_size, bold=True)
                winner_text = font.render(f"{self.winner.upper()} WINS!", True, GOLD)
                text_rect = winner_text.get_rect(center=(BOARD_SIZE // 2, BOARD_SIZE // 4))
                surface.blit(winner_text, text_rect)
                
                # Load and draw golden chainsaw image
                chainsaw_path = IMAGE_DIR / 'golden_chainsaw.jpg'
                if os.path.exists(chainsaw_path):
                    chainsaw = pygame.image.load(str(chainsaw_path))
                    
                    # Make chainsaw image larger
                    chainsaw_size = min(int(BOARD_SIZE * 0.6), 600)  # 60% of board size, max 600px
                    chainsaw_surface = pygame.transform.scale(chainsaw, (chainsaw_size, chainsaw_size))
                    
                    # Center the chainsaw image
                    chainsaw_rect = chainsaw_surface.get_rect(center=(BOARD_SIZE // 2, BOARD_SIZE // 2 + SQUARE_SIZE))
                    surface.blit(chainsaw_surface, chainsaw_rect)
            except Exception as e:
                print(f"Error drawing winner screen: {e}")

        # Draw capture meme if a piece was just captured and waiting for click
        if self.captured_piece and self.waiting_for_click:
            self.captured_piece.draw_capture_meme(surface)

        # Draw winner message and trophy
        if self.game_over and self.winner:
            # Draw semi-transparent overlay
            overlay = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            surface.blit(overlay, (0, 0))
            
            # Draw winner text
            font = pygame.font.SysFont('Arial', 48)
            color_name = "Republicans" if self.winner == 'red' else "Democrats"
            text = f"{color_name} win the Golden Chainsaw!"
            text_surface = font.render(text, True, RED if self.winner == 'red' else BLUE)
            text_rect = text_surface.get_rect(center=(WINDOW_SIZE//2, WINDOW_SIZE//3))
            surface.blit(text_surface, text_rect)
            
            # Draw golden chainsaw trophy
            if self._winner_surface:
                trophy_rect = self._winner_surface.get_rect(center=(WINDOW_SIZE//2, 2*WINDOW_SIZE//3))
                surface.blit(self._winner_surface, trophy_rect)

    def get_piece_at(self, x: int, y: int) -> Optional[ChessPiece]:
        if 0 <= x < 8 and 0 <= y < 8:
            return self.board[y][x]
        return None

    def is_valid_move(self, piece: ChessPiece, new_x: int, new_y: int) -> bool:
        if not (0 <= new_x < 8 and 0 <= new_y < 8):
            return False

        target = self.get_piece_at(new_x, new_y)
        if target and target.color == piece.color:
            return False

        dx = new_x - piece.x
        dy = new_y - piece.y

        if piece.piece_type == 'pawn':
            direction = 1 if piece.color == 'red' else -1
            # Normal move
            if dx == 0 and dy == direction and not target:
                return True
            # Initial double move
            if dx == 0 and dy == 2 * direction and not piece.has_moved and not target:
                intermediate = self.get_piece_at(piece.x, piece.y + direction)
                return not intermediate
            # Capture
            if abs(dx) == 1 and dy == direction and target:
                return True
            return False

        elif piece.piece_type == 'rook':
            return (dx == 0 or dy == 0) and self._is_path_clear(piece.x, piece.y, new_x, new_y)

        elif piece.piece_type == 'knight':
            return (abs(dx) == 2 and abs(dy) == 1) or (abs(dx) == 1 and abs(dy) == 2)

        elif piece.piece_type == 'bishop':
            return abs(dx) == abs(dy) and self._is_path_clear(piece.x, piece.y, new_x, new_y)

        elif piece.piece_type == 'queen':
            return (dx == 0 or dy == 0 or abs(dx) == abs(dy)) and \
                   self._is_path_clear(piece.x, piece.y, new_x, new_y)

        elif piece.piece_type == 'king':
            return abs(dx) <= 1 and abs(dy) <= 1

        return False

    def _is_path_clear(self, x1: int, y1: int, x2: int, y2: int) -> bool:
        dx = x2 - x1
        dy = y2 - y1
        
        if dx == 0:  # Vertical movement
            step = 1 if dy > 0 else -1
            for y in range(y1 + step, y2, step):
                if self.get_piece_at(x1, y):
                    return False
        elif dy == 0:  # Horizontal movement
            step = 1 if dx > 0 else -1
            for x in range(x1 + step, x2, step):
                if self.get_piece_at(x, y1):
                    return False
        else:  # Diagonal movement
            step_x = 1 if dx > 0 else -1
            step_y = 1 if dy > 0 else -1
            x, y = x1 + step_x, y1 + step_y
            while x != x2 and y != y2:
                if self.get_piece_at(x, y):
                    return False
                x += step_x
                y += step_y
        return True

    def move_piece(self, piece: ChessPiece, new_x: int, new_y: int):
        # Capture piece if present
        target = self.get_piece_at(new_x, new_y)
        if target:
            # Store captured piece for meme display
            self.captured_piece = target
            self.capture_time = pygame.time.get_ticks()
            self.waiting_for_click = True  # Set flag to wait for click
            self.captured_pieces.append(target)  # Add to captured pieces list
            
            # Check for game over
            if target.piece_type == 'king':
                self.game_over = True
                self.winner = piece.color

        # Update board
        self.board[piece.y][piece.x] = None
        self.board[new_y][new_x] = piece
        piece.x = new_x
        piece.y = new_y
        piece.has_moved = True

    def handle_click(self, pos: Tuple[int, int]):
        try:
            # Get click position relative to board
            board_x = pos[0] - BOARD_OFFSET_X
            board_y = pos[1] - BOARD_OFFSET_Y
            
            # Check if click is outside the board
            if board_x < 0 or board_x >= BOARD_SIZE or board_y < 0 or board_y >= BOARD_SIZE:
                self.selected_piece = None  # Deselect if clicking outside
                return
            
            # Convert to board coordinates
            x = board_x // SQUARE_SIZE
            y = board_y // SQUARE_SIZE
            
            # Ensure valid board position
            if not (0 <= x < 8 and 0 <= y < 8):
                self.selected_piece = None
                return
            
            # If waiting for click after capture, clear capture state
            if self.waiting_for_click and self.captured_piece:
                self.captured_piece = None
                self.waiting_for_click = False
                return
            
            clicked_piece = self.get_piece_at(x, y)
            
            # If a piece is already selected
            if self.selected_piece:
                # If clicking the same piece, deselect it
                if clicked_piece == self.selected_piece:
                    self.selected_piece = None
                # If clicking a valid move location
                elif self.is_valid_move(self.selected_piece, x, y):
                    self.move_piece(self.selected_piece, x, y)
                    self.selected_piece = None
                    if not self.waiting_for_click:  # Only change turn if not showing capture
                        self.turn = 'blue' if self.turn == 'red' else 'red'
                # If clicking a different piece of same color, select it
                elif clicked_piece and clicked_piece.color == self.turn:
                    self.selected_piece = clicked_piece
                # If clicking invalid location, deselect
                else:
                    self.selected_piece = None
            # If no piece selected and clicking own piece, select it
            elif clicked_piece and clicked_piece.color == self.turn:
                self.selected_piece = clicked_piece
        except Exception as e:
            print(f"Error handling click: {e}")
            self.selected_piece = None  # Reset selection on error

def draw_left_panel(screen, game):
    global IS_MUTED, MUSIC_VOLUME
    
    # Left panel background
    pygame.draw.rect(screen, (40, 40, 40), (0, 0, LEFT_PANEL_WIDTH, WINDOW_HEIGHT))
    
    # Draw volume/mute button in left panel
    button_x = (LEFT_PANEL_WIDTH - MUSIC_BUTTON_SIZE) // 2
    button_y = 10
    button_rect = pygame.Rect(button_x, button_y, MUSIC_BUTTON_SIZE, MUSIC_BUTTON_SIZE)
    
    # Draw button background
    pygame.draw.rect(screen, (200, 200, 200), button_rect, border_radius=5)
    
    # Draw icon (simple speaker symbol)
    icon_color = (100, 100, 100) if IS_MUTED else (50, 50, 50)
    pygame.draw.polygon(screen, icon_color, [
        (button_x + 10, button_y + MUSIC_BUTTON_SIZE//2),
        (button_x + 20, button_y + 10),
        (button_x + 20, button_y + 30),
    ])
    
    if not IS_MUTED:
        # Draw sound waves when not muted
        for i in range(2):
            x = button_x + 25 + i * 5
            pygame.draw.arc(screen, icon_color,
                          (x, button_y + 15, 5, 10),
                          -1.5, 1.5, 2)
    
    # Draw volume slider
    slider_y = button_y + MUSIC_BUTTON_SIZE + 10
    slider_width = LEFT_PANEL_WIDTH * 0.8
    slider_rect = pygame.Rect((LEFT_PANEL_WIDTH - slider_width) // 2, slider_y, slider_width, 20)
    pygame.draw.rect(screen, (180, 180, 180), slider_rect, border_radius=5)
    volume_width = int(slider_rect.width * MUSIC_VOLUME)
    volume_rect = pygame.Rect(slider_rect.x, slider_rect.y, volume_width, slider_rect.height)
    pygame.draw.rect(screen, (100, 100, 100), volume_rect, border_radius=5)
    
    # Draw captured pieces list title
    title_y = slider_y + 50
    font = pygame.font.SysFont('Arial', 20, bold=True)
    title = font.render('Captured Pieces', True, WHITE)
    title_rect = title.get_rect(centerx=LEFT_PANEL_WIDTH//2, y=title_y)
    screen.blit(title, title_rect)
    
    # Draw captured pieces list
    list_y = title_y + 40
    item_height = 30
    item_padding = 5
    name_font = pygame.font.SysFont('Arial', 16)
    
    # Get mouse position for hover effect
    mouse_pos = pygame.mouse.get_pos()
    hovered_piece = None
    
    # Draw each captured piece name
    for i, piece in enumerate(game.captured_pieces):
        item_rect = pygame.Rect(5, list_y + i * (item_height + item_padding), 
                               LEFT_PANEL_WIDTH - 10, item_height)
        
        # Check if mouse is hovering over this item
        if item_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (60, 60, 60), item_rect, border_radius=3)
            hovered_piece = piece
        
        name_text = name_font.render(piece.name, True, WHITE)
        name_rect = name_text.get_rect(midleft=(10, item_rect.centery))
        screen.blit(name_text, name_rect)
    
    # Draw hovered piece's meme
    if hovered_piece and hovered_piece._meme_surface:
        meme_size = min(LEFT_PANEL_WIDTH * 1.5, WINDOW_HEIGHT * 0.3)
        scaled_meme = pygame.transform.scale(hovered_piece._meme_surface, 
                                           (meme_size, meme_size))
        meme_rect = scaled_meme.get_rect(center=mouse_pos)
        
        # Ensure meme stays within screen bounds
        if meme_rect.right > WINDOW_WIDTH:
            meme_rect.right = WINDOW_WIDTH
        if meme_rect.bottom > WINDOW_HEIGHT:
            meme_rect.bottom = WINDOW_HEIGHT
        
        screen.blit(scaled_meme, meme_rect)
    
    return button_rect, slider_rect

def handle_music_controls(pos, button_rect, slider_rect):
    global IS_MUTED, MUSIC_VOLUME
    
    if button_rect.collidepoint(pos):
        IS_MUTED = not IS_MUTED
        pygame.mixer.music.set_volume(0.0 if IS_MUTED else MUSIC_VOLUME)
        return True
    
    if slider_rect.collidepoint(pos):
        MUSIC_VOLUME = (pos[0] - slider_rect.x) / slider_rect.width
        MUSIC_VOLUME = max(0.0, min(1.0, MUSIC_VOLUME))  # Clamp between 0 and 1
        if not IS_MUTED:
            pygame.mixer.music.set_volume(MUSIC_VOLUME)
        return True
    
    return False

def main():
    global WINDOW_SIZE, BOARD_SIZE, SQUARE_SIZE, PIECE_SIZE, PORTRAIT_SIZE, IS_MUTED, MUSIC_VOLUME
    
    pygame.init()  # Make sure pygame is initialized
    
    # Start background music if file exists
    if BACKGROUND_MUSIC.exists():
        try:
            pygame.mixer.music.load(str(BACKGROUND_MUSIC))
            pygame.mixer.music.set_volume(MUSIC_VOLUME)
            pygame.mixer.music.play(-1)  # -1 means loop indefinitely
        except Exception as e:
            print(f"Error loading background music: {e}")
    
    clock = pygame.time.Clock()
    game = ChessGame()

    # Set initial window size
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Political Chess")
    
    # Initialize board dimensions
    update_sizes(WINDOW_WIDTH, WINDOW_HEIGHT)
    
    # New Game button properties
    button_width = 200
    button_height = 50
    button_color = (50, 205, 50)  # Green color
    button_hover_color = (34, 139, 34)  # Darker green
    button_text = "New Game"
    button_font = None
    button_rect = None
    
    running = True
    while running:
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.VIDEORESIZE:
                    # Get new window size, ensuring minimum dimensions
                    new_width = max(event.w, MIN_WINDOW_WIDTH)
                    new_height = max(event.h, MIN_WINDOW_HEIGHT)
                    
                    # Update the screen and all size-dependent variables
                    screen = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)
                    update_sizes(new_width, new_height)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Get mouse position
                    mouse_pos = pygame.mouse.get_pos()
                    
                    # Get music control areas
                    music_button, slider = draw_left_panel(screen, game)
                    
                    # Check if click was on music controls
                    if handle_music_controls(mouse_pos, music_button, slider):
                        continue
                    
                    if game.game_over and button_rect and button_rect.collidepoint(mouse_pos):
                        # Reset game if New Game button is clicked
                        game = ChessGame()
                    else:
                        # Handle regular game clicks
                        game.handle_click(mouse_pos)

            # Fill background
            screen.fill(BLACK)
            
            # Create and draw board surface
            board_surface = pygame.Surface((BOARD_SIZE, BOARD_SIZE))
            game.draw(board_surface)
            
            # Position the board after left panel
            screen.blit(board_surface, (BOARD_OFFSET_X, BOARD_OFFSET_Y))
            
            # Draw left panel with music controls and captured pieces list
            draw_left_panel(screen, game)
            
            # Draw New Game button if game is over
            if game.game_over:
                # Create button font
                if not button_font:
                    button_font = pygame.font.SysFont('Arial', int(button_height * 0.6), bold=True)
                
                # Create button
                button_rect = pygame.Rect((current_size - button_width) // 2,
                                         current_size - button_height - margin // 2,
                                         button_width, button_height)
                
                # Check if mouse is hovering over button
                mouse_pos = pygame.mouse.get_pos()
                color = button_hover_color if button_rect.collidepoint(mouse_pos) else button_color
                
                # Draw button
                pygame.draw.rect(screen, color, button_rect, border_radius=int(button_height * 0.2))
                
                # Draw button text
                text = button_font.render(button_text, True, WHITE)
                text_rect = text.get_rect(center=button_rect.center)
                screen.blit(text, text_rect)
            else:
                # Reset button font when starting new game
                button_font = None
            
            # Update display
            pygame.display.flip()
            clock.tick(60)
            
        except Exception as e:
            print(f"Error: {e}")
            continue
    
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
