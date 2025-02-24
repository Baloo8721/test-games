from flask import Flask, render_template, request, jsonify
import pygame
from political_chess import *
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

# Initialize game state
current_game = None

@app.route('/')
def home():
    return render_template('index.html')

@socketio.on('start_game')
def handle_start_game():
    global current_game
    current_game = ChessGame()  # Assuming you have a ChessGame class in political_chess.py
    socketio.emit('game_started', {'message': 'Game started'})

@socketio.on('make_move')
def handle_make_move(data):
    global current_game
    move = data['move']
    result = current_game.make_move(move)  # Assuming make_move is a method in your ChessGame class
    socketio.emit('move_made', {'message': result})

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5001)
