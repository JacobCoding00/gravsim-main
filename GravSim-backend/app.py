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

planets = [Planet(0,0,0.6,600,100),Planet(0,0,0.6,600,700),Planet(0,0,0.6,300,700)]
alive_planets = planets[:] # store a copy of planets
eliminated_planets_index = [] # indexes of all eliminated planets
play = False


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
    print("game started")
    global play
    play = True
    while (play):
        for i in range(2): # do gravity calculation time step 2 times for finer resolution
            gravityCalculator.calculate_gravity(alive_planets, 2)
        planet_positions = []

        # tell frontend that a planet is eliminated
        for i in alive_planets:
            if i.is_eliminated():
                alive_planets.remove(i)
                eliminated_planets_index.append(planets.index(i))
                emit('planet_eliminated', eliminated_planets_index)
                print("eliminated planets", eliminated_planets_index)

        # if one or fewer planets remain, end simulation
        if len(alive_planets) <= 1:
            play = False

        # append array that is sent to frontend with new position vectors
        for i in planets:
            planet_positions.append(i.get_position_vector + i.get_angle_and_speed + [i.get_mass])
        emit('planet_positions', planet_positions)
        print("planet positions sent", planet_positions)
        time.sleep(0.016) # 60 updates per second


@socketio.on('stop')
def stop_sim():
    global play
    play = False


@socketio.on('reset')
def reset_sim():
    global planets
    global alive_planets
    global eliminated_planets_index
    planets = [Planet(40,0,0,500,500),Planet(10,0,0.2,600,700),Planet(3,0,-0.5,300,700),Planet(4,0,0.4,100,700),Planet(3,0,-0.2,210,700)]
    alive_planets = planets[:]
    eliminated_planets_index = []


# When the client disconnects
@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app, debug=True)