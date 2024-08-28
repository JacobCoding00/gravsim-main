from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import gravityCalculator
from planet import Planet
import time
import json

app = Flask(__name__)
CORS(app)

planets = [Planet(100,-0.5,0,700,900),Planet(100,0.5,0,700,600),Planet(0,0.24,0,700,50)]


@app.route('/api/data', methods=['GET'])
def get_data():
    gravityCalculator.calculate_gravity(planets, 0.5)
    planet_positions = []
    for i in planets:
        planet_positions.append(i.get_position_vector)
    data = {'message': planet_positions}
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)