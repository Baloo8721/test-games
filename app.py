from flask import Flask, jsonify, request, render_template
from flask_socketio import SocketIO, emit
from political_chess import ChessGame, ChessPiece
import json

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Store active games
games = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('create_game')
def create_game(data):
    game_id = data.get('game_id')
    if game_id not in games:
        games[game_id] = ChessGame()
        emit('game_created', {'game_id': game_id})

@socketio.on('join_game')
def join_game(data):
    game_id = data.get('game_id')
    if game_id in games:
        emit('game_joined', {'game_id': game_id})
    else:
        emit('error', {'message': 'Game not found'})

@socketio.on('make_move')
def make_move(data):
    game_id = data.get('game_id')
    from_pos = data.get('from')
    to_pos = data.get('to')
    
    if game_id in games:
        game = games[game_id]
        piece = game.get_piece_at(from_pos[0], from_pos[1])
        if piece and game.is_valid_move(piece, to_pos[0], to_pos[1]):
            game.move_piece(piece, to_pos[0], to_pos[1])
            emit('move_made', {
                'game_id': game_id,
                'from': from_pos,
                'to': to_pos,
                'turn': game.turn
            }, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
