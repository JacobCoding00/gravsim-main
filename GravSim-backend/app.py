from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, send, emit
import gravityCalculator
from planet import Planet
import time
import json

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

planets = [Planet(0,-0.5,0,700,900),Planet(100,0,0,700,400)]


@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('message', {'data': 'Hello from Flask WebSocket!'}) # Send data when client connects


# When the server receives a message from a client
@socketio.on('message')
def handle_message(message):
    print('Received message:', message)
    send(f"Server received: {message}")  # Echo the message back to the client

# When the server receives the start command from the client
@socketio.on('start')
def start_sim():
    while (True):
        gravityCalculator.calculate_gravity(planets, 1)
        planet_positions = []
        for i in planets:
            planet_positions.append(i.get_position_vector)
        emit('planet_positions', planet_positions)
        print("planet positions sent", planet_positions)
        time.sleep(0.01)

# When the client disconnects
@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, debug=True)