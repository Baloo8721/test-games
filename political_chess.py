import pygame
import sys
import os
from typing import Optional, Tuple, List, Dict
from pathlib import Path

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = 1000
BOARD_SIZE = 900
SQUARE_SIZE = BOARD_SIZE // 8
PIECE_SIZE = SQUARE_SIZE - 20
PORTRAIT_SIZE = 200
BOARD_OFFSET = (WINDOW_SIZE - BOARD_SIZE) // 2  # Center the board
HOVER_DELAY = 500  # milliseconds before showing portrait
CAPTURE_DISPLAY_TIME = 2000  # milliseconds to show capture meme

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 50, 50)
BLUE = (50, 50, 220)
BOARD_LIGHT = (255, 255, 255)  # White squares
BOARD_DARK = (128, 128, 128)   # Grey squares
HIGHLIGHT = (255, 255, 0, 128)

# Paths
IMAGE_DIR = Path('/Users/tylerbelisle/CascadeProjects/political_chess/images')
ASSETS_DIR = Path('/Users/tylerbelisle/CascadeProjects/political_chess/assets')

# Screen setup
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE), pygame.RESIZABLE)
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
        {'name': 'Kash Patel', 'portrait': 'patel.jpg', 'meme': 'patel_meme.jpg'}  # TODO: Add these images
    ],
    'pawn': [
        {'name': 'Matt Gaetz', 'portrait': 'gaetz.jpg', 'meme': 'gaetz_meme.jpg'},
        {'name': 'RFK Jr', 'portrait': 'rfk.jpg', 'meme': 'rfk_meme.jpg'},  # TODO: Add these images
        {'name': 'Marjorie T Greene', 'portrait': 'greene.jpg', 'meme': 'greene_meme.jpg'},
        {'name': 'Josh Hawley', 'portrait': 'hawley.jpg', 'meme': 'hawley_meme.jpg'},
        {'name': 'Jim Jordan', 'portrait': 'jordan.jpg', 'meme': 'jordan_meme.jpg'},
        {'name': 'Lauren Boebert', 'portrait': 'boebert.jpg', 'meme': 'boebert_meme.jpg'},
        {'name': 'Greg Abbott', 'portrait': 'abbott.jpg', 'meme': 'abbott_meme.jpg'},
        {'name': 'Tim Scott', 'portrait': 'scott.jpg', 'meme': 'scott_meme.jpg'}
    ]
}

BLUE_PIECES = {
    'king': {'name': 'Joe Biden', 'portrait': 'biden.jpg', 'meme': 'biden_meme.jpg'},
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
        {'name': 'Barack Obama', 'portrait': 'obama.jpg', 'meme': 'obama_meme.jpg'},
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
            portrait_path = IMAGE_DIR / self.portrait
            meme_path = IMAGE_DIR / self.meme
            
            # Check if files exist first
            if not portrait_path.exists():
                print(f"Missing portrait for {self.name}: {self.portrait} - Please add this image to the images directory")
                return
                
            if not meme_path.exists():
                print(f"Missing meme for {self.name}: {self.meme} - Please add this image to the images directory")
                return
            
            # Load portrait
            try:
                portrait_img = pygame.image.load(str(portrait_path))
                self._portrait_surface = pygame.transform.scale(portrait_img, (SQUARE_SIZE, SQUARE_SIZE))  # Exactly fill square
            except Exception as e:
                print(f"Error loading portrait for {self.name}: {e}")
            
            # Load meme
            try:
                meme_img = pygame.image.load(str(meme_path))
                self._meme_surface = pygame.transform.scale(meme_img, (PORTRAIT_SIZE, PORTRAIT_SIZE))
            except Exception as e:
                print(f"Error loading meme for {self.name}: {e}")
                
        except Exception as e:
            print(f"Error loading images for {self.name}: {e}")

    def draw_shape(self, surface: pygame.Surface):
        center_x = self.x * SQUARE_SIZE + SQUARE_SIZE // 2
        center_y = self.y * SQUARE_SIZE + SQUARE_SIZE // 2

        # Load piece image if not already loaded
        if not hasattr(self, '_piece_surface'):
            piece_image_path = ASSETS_DIR / f"{self.piece_type}_{self.color}.png"
            try:
                self._piece_surface = pygame.image.load(str(piece_image_path))
                # Scale the image to fit the piece size
                self._piece_surface = pygame.transform.scale(self._piece_surface, (PIECE_SIZE, PIECE_SIZE))
            except Exception as e:
                print(f"Error loading piece image {piece_image_path}: {e}")
                return

        # Calculate position to center the piece
        piece_rect = self._piece_surface.get_rect(center=(center_x, center_y))
        surface.blit(self._piece_surface, piece_rect)

        # Draw name
        font = pygame.font.SysFont('Arial', 11, bold=True)
        name_text = font.render(self.name, True, BLACK)
        text_rect = name_text.get_rect(center=(center_x, center_y + PIECE_SIZE//1.8))
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
            x = (WINDOW_SIZE - PORTRAIT_SIZE) // 2
            y = (WINDOW_SIZE - PORTRAIT_SIZE) // 2
            surface.blit(self._meme_surface, (x, y))

    def draw(self, surface: pygame.Surface):
        # Draw the piece shape
        self.draw_shape(surface)

        # Check for hover
        mouse_x, mouse_y = pygame.mouse.get_pos()
        piece_rect = pygame.Rect(self.x * SQUARE_SIZE, self.y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        
        # Only show portrait when hovering over the piece's square
        if piece_rect.collidepoint(mouse_x, mouse_y):
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
        self.captured_piece: Optional[ChessPiece] = None
        self.capture_time = 0
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
            # Highlight selected piece
            x, y = self.selected_piece.x * SQUARE_SIZE, self.selected_piece.y * SQUARE_SIZE
            highlight_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            pygame.draw.rect(highlight_surface, HIGHLIGHT, 
                           (0, 0, SQUARE_SIZE, SQUARE_SIZE))
            surface.blit(highlight_surface, (x, y))
            
            # Show valid moves
            for y in range(8):
                for x in range(8):
                    if self.is_valid_move(self.selected_piece, x, y):
                        highlight_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                        pygame.draw.rect(highlight_surface, (0, 255, 0, 80), 
                                       (0, 0, SQUARE_SIZE, SQUARE_SIZE))
                        surface.blit(highlight_surface, (x * SQUARE_SIZE, y * SQUARE_SIZE))

        # Draw capture meme if a piece was just captured
        current_time = pygame.time.get_ticks()
        if self.captured_piece and current_time - self.capture_time < CAPTURE_DISPLAY_TIME:
            # Draw semi-transparent overlay
            overlay = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            surface.blit(overlay, (0, 0))
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
        if self.game_over:
            return

        x = pos[0] // SQUARE_SIZE
        y = pos[1] // SQUARE_SIZE

        clicked_piece = self.get_piece_at(x, y)

        if self.selected_piece:
            if self.is_valid_move(self.selected_piece, x, y):
                self.move_piece(self.selected_piece, x, y)
                self.turn = 'blue' if self.turn == 'red' else 'red'
            self.selected_piece = None
        elif clicked_piece and clicked_piece.color == self.turn:
            self.selected_piece = clicked_piece

def main():
    clock = pygame.time.Clock()
    game = ChessGame()

    current_size = WINDOW_SIZE
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                # Update window size
                current_size = min(event.w, event.h)
                screen = pygame.display.set_mode((current_size, current_size), pygame.RESIZABLE)
                # Update game constants based on new size
                global BOARD_SIZE, SQUARE_SIZE, PIECE_SIZE
                BOARD_SIZE = int(current_size * 0.9)  # Board is 90% of window
                SQUARE_SIZE = BOARD_SIZE // 8
                PIECE_SIZE = SQUARE_SIZE - 20
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Adjust mouse position for board margin
                margin = (current_size - BOARD_SIZE) // 2
                adjusted_pos = (event.pos[0] - margin, event.pos[1] - margin)
                if 0 <= adjusted_pos[0] <= BOARD_SIZE and 0 <= adjusted_pos[1] <= BOARD_SIZE:
                    game.handle_click(adjusted_pos)

        # Center the board in the window
        margin = (current_size - BOARD_SIZE) // 2
        screen.fill(BLACK)
        # Create a surface for the board
        board_surface = pygame.Surface((BOARD_SIZE, BOARD_SIZE))
        game.draw(board_surface)
        screen.blit(board_surface, (margin, margin))
        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()
