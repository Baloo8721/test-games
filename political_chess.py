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
            
            # Initialize meme surfaces list and tracking variables
            self._meme_surfaces = []
            self._current_meme_index = 0
            self._last_meme_switch = 0
            self._meme_switch_delay = 1000  # Switch meme every 1 second
            
            # Try to convert AVIF to PNG first
            if self.name in ['Elon Musk', 'Kash Patel']:
                png_path = portrait_path.with_suffix('.png')
                os.system(f'sips -s format png "{portrait_path}" --out "{png_path}"')
                portrait_path = png_path
            
            # Check if portrait exists
            if not portrait_path.exists():
                print(f"Missing portrait for {self.name}: {self.portrait} - Please add this image to the images directory")
                return
            
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
            
            # Load main meme
            main_meme_path = IMAGE_DIR / self.meme
            if main_meme_path.exists():
                try:
                    print(f"Loading main meme: {main_meme_path}")
                    meme_surface = pygame.image.load(str(main_meme_path))
                    self._meme_surfaces.append(meme_surface)
                    print(f"Successfully loaded main meme")
                except Exception as e:
                    print(f"Error loading main meme: {e}")
            
            # Try to load additional meme (meme1)
            base_name = self.meme.rsplit('.', 1)[0]  # Remove extension
            extra_meme_path = IMAGE_DIR / f"{base_name}1.jpg"
            if extra_meme_path.exists():
                try:
                    print(f"Loading extra meme: {extra_meme_path}")
                    meme_surface = pygame.image.load(str(extra_meme_path))
                    self._meme_surfaces.append(meme_surface)
                    print(f"Successfully loaded extra meme")
                except Exception as e:
                    print(f"Error loading extra meme: {e}")
            
            if not self._meme_surfaces:
                print(f"No memes found for {self.name}")
                
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
        if len(self._meme_surfaces) > 0:
            # Create semi-transparent overlay for full window
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))  # Dark overlay for better contrast
            surface.blit(overlay, (0, 0))
            
            # Use first meme for capture display
            capture_meme = self._meme_surfaces[0]
            
            # Get window dimensions
            window_width = surface.get_width()
            window_height = surface.get_height()
            
            # Calculate meme size (maintain aspect ratio)
            meme_width = capture_meme.get_width()
            meme_height = capture_meme.get_height()
            scale = min(window_width * 0.8 / meme_width, window_height * 0.8 / meme_height)
            scaled_width = int(meme_width * scale)
            scaled_height = int(meme_height * scale)
            
            # Scale meme
            scaled_meme = pygame.transform.scale(capture_meme, (scaled_width, scaled_height))
            
            # Center meme on screen
            meme_rect = scaled_meme.get_rect(center=(window_width // 2, window_height // 2))
            surface.blit(scaled_meme, meme_rect)
            
            # Add piece name at top
            name_font_size = int(window_height * 0.06)
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
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.selected_piece = None
        self.turn = 'red'  # red goes first
        self.game_over = False
        self.winner = None
        self.captured_piece = None
        self.capture_time = 0
        self.waiting_for_click = False
        self.captured_pieces = []  # List to track all captured pieces
        self.setup_board()
        
        # Load winner image
        try:
            winner_img = pygame.image.load(str(IMAGE_DIR / 'golden_chainsaw.jpg'))
            self._winner_surface = pygame.transform.scale(winner_img, (PORTRAIT_SIZE, PORTRAIT_SIZE))
        except Exception as e:
            print(f"Error loading winner image: {e}")
            self._winner_surface = None

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
                # Even smaller font size and more aggressive scaling
                winner_font_size = min(int(BOARD_SIZE * 0.06), 54)  # Reduced from 0.08 to 0.06, max 54pt
                font = pygame.font.SysFont('Arial', winner_font_size, bold=True)
                winner_color = BLUE if self.winner == 'blue' else RED
                team_name = "DEMOCRATS" if self.winner == 'blue' else "REPUBLICANS"
                winner_text = font.render(f"{team_name} WIN!", True, winner_color)
                
                # More aggressive width constraint (80% of board width instead of 90%)
                if winner_text.get_width() > BOARD_SIZE * 0.8:  # If text is wider than 80% of board
                    scale = (BOARD_SIZE * 0.8) / winner_text.get_width()
                    winner_font_size = int(winner_font_size * scale)
                    font = pygame.font.SysFont('Arial', winner_font_size, bold=True)
                    winner_text = font.render(f"{team_name} WIN!", True, winner_color)
                
                # Position text slightly higher
                text_rect = winner_text.get_rect(center=(BOARD_SIZE // 2, BOARD_SIZE // 5))
                surface.blit(winner_text, text_rect)
                
                # Load and draw golden chainsaw image
                chainsaw_path = IMAGE_DIR / 'golden_chainsaw.jpg'
                if os.path.exists(chainsaw_path):
                    chainsaw = pygame.image.load(str(chainsaw_path))
                    
                    # Make chainsaw image larger
                    chainsaw_size = min(int(BOARD_SIZE * 0.6), 600)  # 60% of board size, max 600px
                    chainsaw_surface = pygame.transform.scale(chainsaw, (chainsaw_size, chainsaw_size))
                    
                    # Center the chainsaw image
                    chainsaw_rect = chainsaw_surface.get_rect(center=(BOARD_SIZE // 2, BOARD_SIZE // 2))
                    surface.blit(chainsaw_surface, chainsaw_rect)
                    
                    # Draw New Game button
                    button_width = min(int(BOARD_SIZE * 0.3), 300)  # 30% of board width, max 300px
                    button_height = min(int(BOARD_SIZE * 0.1), 80)  # 10% of board height, max 80px
                    button_rect = pygame.Rect(
                        BOARD_SIZE // 2 - button_width // 2,
                        int(BOARD_SIZE * 0.8),  # Position at 80% of board height
                        button_width,
                        button_height
                    )
                    
                    # Button colors
                    button_color = (34, 139, 34)  # Forest green
                    pygame.draw.rect(surface, button_color, button_rect, border_radius=10)
                    pygame.draw.rect(surface, WHITE, button_rect, 3, border_radius=10)
                    
                    # Button text with dynamic sizing
                    button_font_size = min(int(button_height * 0.6), 48)
                    button_font = pygame.font.SysFont('Arial', button_font_size, bold=True)
                    button_text = button_font.render('New Game', True, WHITE)
                    button_text_rect = button_text.get_rect(center=button_rect.center)
                    surface.blit(button_text, button_text_rect)
            except Exception as e:
                print(f"Error drawing winner screen: {e}")

        # Draw capture meme if a piece was just captured and waiting for click
        if self.captured_piece and self.waiting_for_click and not self.game_over:
            self.captured_piece.draw_capture_meme(surface)

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

    def _load_chainsaw(self):
        chainsaw_path = IMAGE_DIR / 'golden_chainsaw.jpg'
        if chainsaw_path.exists():
            try:
                print("Loading golden chainsaw image...")
                self.chainsaw_surface = pygame.image.load(str(chainsaw_path))
                print("Successfully loaded chainsaw image")
            except Exception as e:
                print(f"Error loading chainsaw: {e}")
                self.chainsaw_surface = None
    
    def move_piece(self, piece: ChessPiece, new_x: int, new_y: int):
        print(f"Moving {piece.color} {piece.piece_type} to {new_x}, {new_y}")
        
        # Get target piece before updating board
        target = self.get_piece_at(new_x, new_y)
        
        # Update board
        self.board[piece.y][piece.x] = None
        self.board[new_y][new_x] = piece
        piece.x = new_x
        piece.y = new_y
        piece.has_moved = True
        
        # Handle capture if there was a piece at the target location
        if target and target != piece:
            print(f"Capturing {target.color} {target.piece_type}!")
            self.captured_pieces.append(target)
            
            if target.piece_type == 'king':
                print("!!! GAME OVER - KING CAPTURED !!!")
                print(f"!!! {piece.color.upper()} TEAM WINS !!!")
                self.game_over = True
                self.winner = piece.color
                self.selected_piece = None
                self.turn = None  # Disable turns
                # Don't return here - let the game continue to show the winner screen
            else:
                # Show capture meme if not game over
                if len(target._meme_surfaces) > 0:
                    self.captured_piece = target
                    self.capture_time = pygame.time.get_ticks()
                    self.waiting_for_click = True
        
        # Switch turns if game is not over
        if not self.game_over:
            self.turn = 'blue' if self.turn == 'red' else 'red'

    def handle_click(self, pos: Tuple[int, int]):
        try:
            print("\n=== HANDLING CLICK ===")
            print(f"Game over: {self.game_over}")
            print(f"Current turn: {self.turn}")
            
            # If game is over, check for new game button click
            if self.game_over and self.winner:
                print("Game is over, checking for new game click")
                screen_width, screen_height = pygame.display.get_surface().get_size()
                button_width = min(300, screen_width * 0.3)
                button_height = min(80, screen_height * 0.1)
                button_rect = pygame.Rect(
                    screen_width // 2 - button_width // 2,
                    screen_height * 0.8,
                    button_width,
                    button_height
                )
                if button_rect.collidepoint(pos):
                    print("New game button clicked!")
                    self.__init__()  # Reset the game completely
                    self.game_over = False
                    self.winner = None
                    self.turn = 'red'
                    return
                return  # Just return, don't process any other clicks when game is over
            
            # Get click position relative to board
            board_x = pos[0] - BOARD_OFFSET_X
            board_y = pos[1] - BOARD_OFFSET_Y
            
            # Check if click is outside the board
            if board_x < 0 or board_x >= BOARD_SIZE or board_y < 0 or board_y >= BOARD_SIZE:
                print("Click outside board")
                self.selected_piece = None
                return
            
            # Convert to board coordinates
            x = board_x // SQUARE_SIZE
            y = board_y // SQUARE_SIZE
            print(f"Board coordinates: {x}, {y}")
            
            # If waiting for click after capture, clear capture state
            if self.waiting_for_click and self.captured_piece:
                print("Clearing capture state")
                self.captured_piece = None
                self.waiting_for_click = False
                # Don't return here - allow the next move
            
            clicked_piece = self.get_piece_at(x, y)
            if clicked_piece:
                print(f"Clicked on {clicked_piece.color} {clicked_piece.piece_type}")
            
            # If a piece is already selected
            if self.selected_piece:
                print(f"Selected piece: {self.selected_piece.color} {self.selected_piece.piece_type}")
                # If clicking the same piece, deselect it
                if clicked_piece == self.selected_piece:
                    print("Deselecting piece")
                    self.selected_piece = None
                # If clicking a valid move location
                elif self.is_valid_move(self.selected_piece, x, y):
                    print("Making move...")
                    self.move_piece(self.selected_piece, x, y)
                    self.selected_piece = None
                    print(f"Current turn: {self.turn}")
                # If clicking a different piece of same color, select it
                elif clicked_piece and clicked_piece.color == self.turn:
                    print("Switching to new piece")
                    self.selected_piece = clicked_piece
                # If clicking invalid location, deselect
                else:
                    print("Invalid move, deselecting")
                    self.selected_piece = None
            # If no piece selected and clicking own piece, select it
            elif clicked_piece and clicked_piece.color == self.turn:
                print("Selecting new piece")
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
    if hovered_piece and len(hovered_piece._meme_surfaces) > 0:
        # Check if it's time to switch memes
        current_time = pygame.time.get_ticks()
        if current_time - hovered_piece._last_meme_switch >= hovered_piece._meme_switch_delay:
            hovered_piece._current_meme_index = (hovered_piece._current_meme_index + 1) % len(hovered_piece._meme_surfaces)
            hovered_piece._last_meme_switch = current_time
        
        # Get current meme
        current_meme = hovered_piece._meme_surfaces[hovered_piece._current_meme_index]
        
        # Scale and display meme
        meme_size = min(LEFT_PANEL_WIDTH * 1.5, WINDOW_HEIGHT * 0.3)
        scaled_meme = pygame.transform.scale(current_meme, (meme_size, meme_size))
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
    global BOARD_SIZE, SQUARE_SIZE, PIECE_SIZE, PORTRAIT_SIZE, IS_MUTED, MUSIC_VOLUME
    
    # Initialize pygame
    if not pygame.get_init():
        pygame.init()
    if not pygame.mixer.get_init():
        pygame.mixer.init()
    
    # Load chainsaw image
    chainsaw_path = IMAGE_DIR / 'golden_chainsaw.jpg'
    chainsaw_surface = None
    try:
        if chainsaw_path.exists():
            chainsaw_surface = pygame.image.load(str(chainsaw_path))
            chainsaw_surface = pygame.transform.scale(chainsaw_surface, (400, 300))
    except Exception as e:
        print(f"Warning: Could not load chainsaw image: {e}")
    
    # Start background music
    try:
        if BACKGROUND_MUSIC.exists():
            pygame.mixer.music.load(str(BACKGROUND_MUSIC))
            pygame.mixer.music.set_volume(MUSIC_VOLUME)
            pygame.mixer.music.play(-1)
    except Exception as e:
        print(f"Warning: Could not load background music: {e}")
    
    clock = pygame.time.Clock()
    game = ChessGame()
    
    # Set initial window size
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Political Chess")
    
    # Initialize board dimensions
    update_sizes(WINDOW_WIDTH, WINDOW_HEIGHT)
    
    # Main game loop
    running = True
    while running:
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                elif event.type == pygame.VIDEORESIZE:
                    new_width = max(event.w, MIN_WINDOW_WIDTH)
                    new_height = max(event.h, MIN_WINDOW_HEIGHT)
                    screen = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)
                    update_sizes(new_width, new_height)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    game.handle_click(event.pos)
            
            # Clear screen and draw game state
            screen.fill(BLACK)
            board_surface = pygame.Surface((BOARD_SIZE, BOARD_SIZE))
            game.draw(board_surface)
            screen.blit(board_surface, (BOARD_OFFSET_X, BOARD_OFFSET_Y))
            draw_left_panel(screen, game)
            
            # Draw capture meme if needed
            if game.captured_piece and game.waiting_for_click and not game.game_over:
                game.captured_piece.draw_capture_meme(screen)
            
            # Draw winner screen if game is over
            if game.game_over and game.winner:
                # Semi-transparent overlay
                overlay = pygame.Surface(screen.get_size())
                overlay.fill(BLACK)
                overlay.set_alpha(180)
                screen.blit(overlay, (0, 0))
                
                # Get current dimensions
                screen_width = screen.get_width()
                screen_height = screen.get_height()
                
                # Draw chainsaw with scaling based on screen size
                if chainsaw_surface:
                    chainsaw_width = min(screen_width * 0.4, 400)  # 40% of screen width, max 400px
                    chainsaw_height = chainsaw_width * 0.75  # Maintain aspect ratio
                    scaled_chainsaw = pygame.transform.scale(chainsaw_surface, (int(chainsaw_width), int(chainsaw_height)))
                    chainsaw_rect = scaled_chainsaw.get_rect(center=(screen_width // 2, screen_height // 2))
                    screen.blit(scaled_chainsaw, chainsaw_rect)
                
                # Draw winner text with dynamic sizing
                font_size = min(int(screen_width * 0.15), 150)  # 15% of screen width, max 150px
                winner_font = pygame.font.SysFont('Arial', font_size, bold=True)
                winner_color = BLUE if game.winner == 'blue' else RED
                team_name = "DEMOCRATS" if game.winner == 'blue' else "REPUBLICANS"
                winner_text = winner_font.render(f'{team_name} WIN!', True, winner_color)
                winner_rect = winner_text.get_rect(center=(screen_width // 2, screen_height * 0.2))
                screen.blit(winner_text, winner_rect)
                
                # Draw New Game button
                button_width = min(300, screen_width * 0.3)
                button_height = min(80, screen_height * 0.1)
                button_rect = pygame.Rect(
                    screen_width // 2 - button_width // 2,
                    screen_height * 0.8,  # Position at 80% of screen height
                    button_width,
                    button_height
                )
                
                # Button colors
                button_color = (34, 139, 34)  # Forest green
                pygame.draw.rect(screen, button_color, button_rect, border_radius=10)
                pygame.draw.rect(screen, WHITE, button_rect, 3, border_radius=10)
                
                # Button text with dynamic sizing
                button_font_size = min(int(button_height * 0.6), 48)
                button_font = pygame.font.SysFont('Arial', button_font_size, bold=True)
                button_text = button_font.render('New Game', True, WHITE)
                button_text_rect = button_text.get_rect(center=button_rect.center)
                screen.blit(button_text, button_text_rect)
            
            try:
                # Update display
                pygame.display.flip()
                clock.tick(60)
            except pygame.error:
                break
        except Exception as e:
            print(f"Error in game loop: {e}")
            break
    
    # Clean up
    try:
        pygame.quit()
    except:
        pass

if __name__ == '__main__':
    main()
