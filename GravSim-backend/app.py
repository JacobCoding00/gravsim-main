from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import gravityCalculator
from planet import Planet
import time
import json

app = Flask(__name__)
CORS(app)

planets = [Planet(0,-0.4,0,700,900),Planet(100,0,0,700,400),Planet(0,0.5,0,700,100)]


@app.route('/api/data', methods=['GET'])
def get_data():
    gravityCalculator.calculate_gravity(planets, 1)
    planet_positions = []
    for i in planets:
        planet_positions.append(i.get_position_vector)
    data = {'message': planet_positions}
    return jsonify(data)

"""
@app.route('/stream')
def stream():
    def event_stream():
        while True:
            time.sleep(2)
            gravityCalculator.calculate_gravity([],1)
            planet_positions = []
            for i in planets:
                planet_positions.append(i.get_position_vector)
            json_data = json.dumps(planet_positions)
            json_data_test = json.dumps([100,200])
            yield f"data: {json_data_test}\n\n"
            print("data sent")
            time.sleep(2)

    return Response(event_stream(), mimetype="text/event-stream")
"""

if __name__ == '__main__':
    app.run(debug=True)