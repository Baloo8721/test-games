from http.server import BaseHTTPRequestHandler
from datetime import datetime

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = {
            'status': 'ok',
            'message': 'API is working',
            'path': self.path,
            'timestamp': datetime.now().isoformat()
        }
        
        self.wfile.write(str(response).encode())
