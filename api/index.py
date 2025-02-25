from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import parse_qs, urlparse
from .game_state import ChessGame, games

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlparse(self.path)
        if url.path == '/':
            self.send_json({
                'status': 'ok',
                'message': 'Political Chess API',
                'endpoints': [
                    {'method': 'POST', 'path': '/game/create', 'description': 'Create a new game'},
                    {'method': 'GET', 'path': '/game/{game_id}', 'description': 'Get game state'},
                    {'method': 'POST', 'path': '/game/{game_id}/move', 'description': 'Make a move'}
                ]
            })
        elif url.path.startswith('/game/'):
            game_id = url.path.split('/')[2]
            if game_id in games:
                self.send_json({'status': 'ok', 'game': games[game_id].to_dict()})
            else:
                self.send_error(404, 'Game not found')
        else:
            self.send_error(404, 'Not found')

    def do_POST(self):
        url = urlparse(self.path)
        if url.path == '/game/create':
            content_length = int(self.headers['Content-Length'])
            post_data = json.loads(self.rfile.read(content_length))
            game_id = post_data.get('game_id')
            
            if not game_id:
                self.send_error(400, 'game_id is required')
                return
                
            if game_id in games:
                self.send_error(400, 'Game already exists')
                return
                
            games[game_id] = ChessGame()
            self.send_json({'status': 'created', 'game_id': game_id})
            
        elif url.path.startswith('/game/') and url.path.endswith('/move'):
            game_id = url.path.split('/')[2]
            if game_id not in games:
                self.send_error(404, 'Game not found')
                return
                
            content_length = int(self.headers['Content-Length'])
            move_data = json.loads(self.rfile.read(content_length))
            from_pos = move_data.get('from')
            to_pos = move_data.get('to')
            
            if not from_pos or not to_pos:
                self.send_error(400, 'Invalid move data')
                return
                
            game = games[game_id]
            if game.move_piece(from_pos[0], from_pos[1], to_pos[0], to_pos[1]):
                self.send_json({
                    'status': 'success',
                    'game': game.to_dict()
                })
            else:
                self.send_error(400, 'Invalid move')
        else:
            self.send_error(404, 'Not found')

    def send_json(self, data):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
