from flask import Flask, render_template, send_from_directory, request, redirect, url_for
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_cors import CORS
import os
from pathlib import Path
from political_chess import ChessGame, ChessPiece

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['SECRET_KEY'] = 'political_chess_secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

# Store game states
games = {}
IMAGE_DIR = Path('images')
ASSETS_DIR = Path('assets')

@app.route('/')
def index():
    game_id = request.args.get('game')
    if game_id and game_id in games:
        return render_template('index.html', game_id=game_id)
    return render_template('index.html')

@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory('images', filename)

@app.route('/assets/<path:filename>')
def serve_asset(filename):
    return send_from_directory('assets', filename)

@socketio.on('create_game')
def on_create_game(data):
    game_id = data.get('game_id')
    if game_id not in games:
        games[game_id] = {
            'game': ChessGame(),
            'players': {},
            'current_turn': 'red'
        }
    
    # Assign the first player to red
    games[game_id]['players'][request.sid] = 'red'
    join_room(game_id)
    
    emit('game_created', {
        'game_id': game_id,
        'board': get_board_state(games[game_id]['game']),
        'color': 'red'
    })

@socketio.on('join_game')
def on_join_game(data):
    game_id = data.get('game_id')
    if game_id in games and len(games[game_id]['players']) < 2:
        # Assign the second player to blue
        games[game_id]['players'][request.sid] = 'blue'
        join_room(game_id)
        
        emit('game_joined', {
            'game_id': game_id,
            'board': get_board_state(games[game_id]['game']),
            'color': 'blue'
        })
        
        # Notify the other player
        emit('opponent_joined', {
            'current_turn': games[game_id]['current_turn']
        }, room=game_id)
    else:
        emit('error', {'message': 'Game not found or full'})

@socketio.on('disconnect')
def on_disconnect():
    for game_id in list(games.keys()):
        if request.sid in games[game_id]['players']:
            color = games[game_id]['players'][request.sid]
            del games[game_id]['players'][request.sid]
            
            if not games[game_id]['players']:
                del games[game_id]
            else:
                emit('opponent_left', {
                    'color': color
                }, room=game_id)

def get_board_state(game):
    board_state = []
    for y in range(8):
        row = []
        for x in range(8):
            piece = game.get_piece_at(x, y)
            if piece:
                row.append({
                    'type': piece.piece_type,
                    'color': piece.color,
                    'name': piece.name,
                    'x': x,
                    'y': y
                })
            else:
                row.append(None)
        board_state.append(row)
    return board_state

@socketio.on('make_move')
def on_make_move(data):
    game_id = data.get('game_id')
    if game_id in games:
        game = games[game_id]['game']
        player_color = games[game_id]['players'].get(request.sid)
        
        if player_color == games[game_id]['current_turn']:
            from_x = data.get('from_x')
            from_y = data.get('from_y')
            to_x = data.get('to_x')
            to_y = data.get('to_y')
            
            piece = game.get_piece_at(from_x, from_y)
            if piece and piece.color == player_color and game.is_valid_move(piece, to_x, to_y):
                game.move_piece(piece, to_x, to_y)
                
                # Switch turns
                games[game_id]['current_turn'] = 'blue' if player_color == 'red' else 'red'
                
                # Send updated board state to all players
                emit('move_made', {
                    'board': get_board_state(game),
                    'current_turn': games[game_id]['current_turn']
                }, room=game_id)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
