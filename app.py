from flask import Flask, jsonify, request, render_template
from game_logic import ChessGame

app = Flask(__name__)

# Store active games
games = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/create_game', methods=['POST'])
def create_game():
    game_id = request.json.get('game_id')
    if not game_id:
        return jsonify({'error': 'game_id is required'}), 400
    
    if game_id not in games:
        games[game_id] = ChessGame()
        return jsonify({'status': 'created', 'game_id': game_id})
    return jsonify({'error': 'game already exists'}), 400

@app.route('/api/join_game/<game_id>')
def join_game(game_id):
    if game_id in games:
        game = games[game_id]
        return jsonify({
            'status': 'joined',
            'game_state': game.to_dict()
        })
    return jsonify({'error': 'game not found'}), 404

@app.route('/api/make_move/<game_id>', methods=['POST'])
def make_move(game_id):
    if game_id not in games:
        return jsonify({'error': 'game not found'}), 404

    game = games[game_id]
    move_data = request.json
    from_pos = move_data.get('from')
    to_pos = move_data.get('to')

    if not from_pos or not to_pos:
        return jsonify({'error': 'invalid move data'}), 400

    piece = game.get_piece_at(from_pos[0], from_pos[1])
    if not piece:
        return jsonify({'error': 'no piece at source position'}), 400

    if game.move_piece(piece, to_pos[0], to_pos[1]):
        return jsonify({
            'status': 'success',
            'game_state': game.to_dict()
        })
    return jsonify({'error': 'invalid move'}), 400

if __name__ == '__main__':
    app.run(debug=True)
