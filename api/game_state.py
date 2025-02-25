import json
from typing import Dict, List, Optional

class ChessPiece:
    def __init__(self, piece_type: str, color: str, x: int, y: int):
        self.piece_type = piece_type
        self.color = color
        self.x = x
        self.y = y
        self.has_moved = False

    def to_dict(self):
        return {
            'type': self.piece_type,
            'color': self.color,
            'x': self.x,
            'y': self.y,
            'has_moved': self.has_moved
        }

class ChessGame:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.turn = 'red'
        self.game_over = False
        self.winner = None
        self.setup_board()

    def setup_board(self):
        # Setup pawns
        for x in range(8):
            self.board[1][x] = ChessPiece('pawn', 'blue', x, 1)
            self.board[6][x] = ChessPiece('pawn', 'red', x, 6)

        # Setup other pieces
        piece_order = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
        for x, piece_type in enumerate(piece_order):
            self.board[0][x] = ChessPiece(piece_type, 'blue', x, 0)
            self.board[7][x] = ChessPiece(piece_type, 'red', x, 7)

    def get_piece(self, x: int, y: int) -> Optional[ChessPiece]:
        if 0 <= x < 8 and 0 <= y < 8:
            return self.board[y][x]
        return None

    def move_piece(self, from_x: int, from_y: int, to_x: int, to_y: int) -> bool:
        piece = self.get_piece(from_x, from_y)
        if not piece or piece.color != self.turn:
            return False

        # Basic move validation (can be expanded later)
        if not (0 <= to_x < 8 and 0 <= to_y < 8):
            return False

        # Make the move
        self.board[from_y][from_x] = None
        captured = self.board[to_y][to_x]
        self.board[to_y][to_x] = piece
        piece.x = to_x
        piece.y = to_y
        piece.has_moved = True

        # Check for game over (king capture)
        if captured and captured.piece_type == 'king':
            self.game_over = True
            self.winner = piece.color

        # Switch turns
        self.turn = 'blue' if self.turn == 'red' else 'red'
        return True

    def to_dict(self):
        return {
            'board': [[piece.to_dict() if piece else None for piece in row] for row in self.board],
            'turn': self.turn,
            'game_over': self.game_over,
            'winner': self.winner
        }

# Store active games in memory
games: Dict[str, ChessGame] = {}
