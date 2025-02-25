from typing import Optional, List, Dict, Tuple

class ChessPiece:
    def __init__(self, piece_type: str, color: str, piece_data: dict, x: int, y: int):
        self.piece_type = piece_type
        self.color = color
        self.x = x
        self.y = y
        self.name = piece_data['name']
        self.has_moved = False

    def to_dict(self):
        return {
            'piece_type': self.piece_type,
            'color': self.color,
            'x': self.x,
            'y': self.y,
            'name': self.name,
            'has_moved': self.has_moved
        }

class ChessGame:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.turn = 'red'  # red goes first
        self.game_over = False
        self.winner = None
        self.captured_pieces = []
        self.setup_board()

    def setup_board(self):
        # Piece data without images
        piece_data = {
            'pawn': {'name': 'Pawn'},
            'rook': {'name': 'Rook'},
            'knight': {'name': 'Knight'},
            'bishop': {'name': 'Bishop'},
            'queen': {'name': 'Queen'},
            'king': {'name': 'King'}
        }

        # Setup pawns
        for x in range(8):
            self.board[1][x] = ChessPiece('pawn', 'blue', piece_data['pawn'], x, 1)
            self.board[6][x] = ChessPiece('pawn', 'red', piece_data['pawn'], x, 6)

        # Setup other pieces
        piece_order = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
        for x, piece_type in enumerate(piece_order):
            self.board[0][x] = ChessPiece(piece_type, 'blue', piece_data[piece_type], x, 0)
            self.board[7][x] = ChessPiece(piece_type, 'red', piece_data[piece_type], x, 7)

    def get_piece_at(self, x: int, y: int) -> Optional[ChessPiece]:
        if 0 <= x < 8 and 0 <= y < 8:
            return self.board[y][x]
        return None

    def is_valid_move(self, piece: ChessPiece, new_x: int, new_y: int) -> bool:
        if not (0 <= new_x < 8 and 0 <= new_y < 8):
            return False

        if piece.color != self.turn:
            return False

        target = self.get_piece_at(new_x, new_y)
        if target and target.color == piece.color:
            return False

        dx = new_x - piece.x
        dy = new_y - piece.y

        if piece.piece_type == 'pawn':
            direction = -1 if piece.color == 'red' else 1
            if dy == direction and dx == 0 and not target:
                return True
            if not piece.has_moved and dy == 2 * direction and dx == 0 and not target:
                return True
            if abs(dx) == 1 and dy == direction and target:
                return True
            return False

        if not self._is_path_clear(piece.x, piece.y, new_x, new_y):
            return False

        if piece.piece_type == 'rook':
            return dx == 0 or dy == 0
        elif piece.piece_type == 'knight':
            return (abs(dx) == 2 and abs(dy) == 1) or (abs(dx) == 1 and abs(dy) == 2)
        elif piece.piece_type == 'bishop':
            return abs(dx) == abs(dy)
        elif piece.piece_type == 'queen':
            return dx == 0 or dy == 0 or abs(dx) == abs(dy)
        elif piece.piece_type == 'king':
            return abs(dx) <= 1 and abs(dy) <= 1

        return False

    def _is_path_clear(self, x1: int, y1: int, x2: int, y2: int) -> bool:
        dx = x2 - x1
        dy = y2 - y1
        
        if dx == 0 and dy == 0:
            return True

        step_x = 0 if dx == 0 else dx // abs(dx)
        step_y = 0 if dy == 0 else dy // abs(dy)

        x, y = x1 + step_x, y1 + step_y
        while x != x2 or y != y2:
            if self.get_piece_at(x, y):
                return False
            x += step_x
            y += step_y

        return True

    def move_piece(self, piece: ChessPiece, new_x: int, new_y: int) -> bool:
        if not self.is_valid_move(piece, new_x, new_y):
            return False

        target = self.get_piece_at(new_x, new_y)
        if target:
            self.captured_pieces.append(target)

        self.board[piece.y][piece.x] = None
        self.board[new_y][new_x] = piece
        piece.x = new_x
        piece.y = new_y
        piece.has_moved = True

        # Check for game over (king capture)
        if target and target.piece_type == 'king':
            self.game_over = True
            self.winner = piece.color

        self.turn = 'blue' if self.turn == 'red' else 'red'
        return True

    def to_dict(self):
        return {
            'board': [[piece.to_dict() if piece else None for piece in row] for row in self.board],
            'turn': self.turn,
            'game_over': self.game_over,
            'winner': self.winner,
            'captured_pieces': [piece.to_dict() for piece in self.captured_pieces]
        }
