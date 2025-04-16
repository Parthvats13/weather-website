import requests
import json
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

API_KEY = "ef5b69790ad360980aa1e3f7f111425b"
MY_LAT = 56
MY_LNG = 26

def fetch_weather_data():
    parameters = {
        "lat": MY_LAT,
        "lon": MY_LNG,
        "appid": API_KEY,
        "cnt": 4
    }
    response = requests.get("https://api.openweathermap.org/data/2.5/forecast", params=parameters)
    response.raise_for_status()
    weather_data = response.json()
    
    # Save weather data to a JSON file
    with open('weather_data.json', 'w') as file:
        json.dump(weather_data, file, indent=4)
    
    return weather_data

@app.route('/api/weather', methods=['GET'])
def get_weather():
    try:
        weather_data = fetch_weather_data()
        return jsonify(weather_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)