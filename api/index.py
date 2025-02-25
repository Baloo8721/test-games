from http.server import BaseHTTPRequestHandler
import json

def handler(request):
    if request.method == 'GET':
        return {
            'statusCode': 200,
            'body': json.dumps({
                'status': 'ok',
                'message': 'API is working',
                'endpoints': [
                    {'method': 'POST', 'path': '/api/create_game', 'description': 'Create a new game'},
                    {'method': 'GET', 'path': '/api/join_game/<game_id>', 'description': 'Join an existing game'},
                    {'method': 'POST', 'path': '/api/make_move/<game_id>', 'description': 'Make a move'}
                ]
            })
        }
