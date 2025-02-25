from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__, static_folder='../', template_folder='../templates')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)
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
