import requests
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from models import Session, Location

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

API_KEY = "ef5b69790ad360980aa1e3f7f111425b"

def fetch_weather_data(lat, lng):
    parameters = {
        "lat": lat,
        "lon": lng,
        "appid": API_KEY,
        "cnt": 4
    }
    response = requests.get("https://api.openweathermap.org/data/2.5/forecast", params=parameters)
    response.raise_for_status()
    weather_data = response.json()
    
    # Save weather data to a JSON file
    with open(f'weather_data_{lat}_{lng}.json', 'w') as file:
        json.dump(weather_data, file, indent=4)
    
    return weather_data

@app.route('/api/weather', methods=['GET'])
def get_weather():
    try:
        location_id = request.args.get('location_id', type=int)
        session = Session()
        
        if location_id:
            location = session.query(Location).filter_by(id=location_id).first()
            if not location:
                return jsonify({"error": "Location not found"}), 404
            weather_data = fetch_weather_data(location.latitude, location.longitude)
        else:
            # Default to first location if no location_id provided
            location = session.query(Location).first()
            if not location:
                return jsonify({"error": "No locations available"}), 404
            weather_data = fetch_weather_data(location.latitude, location.longitude)
        
        session.close()
        return jsonify(weather_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/locations', methods=['GET'])
def get_locations():
    try:
        session = Session()
        locations = session.query(Location).all()
        session.close()
        return jsonify([location.to_dict() for location in locations])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/locations', methods=['POST'])
def add_location():
    try:
        data = request.json
        session = Session()
        
        location = Location(
            name=data['name'],
            latitude=data['latitude'],
            longitude=data['longitude']
        )
        
        session.add(location)
        session.commit()
        session.close()
        
        return jsonify({"message": "Location added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)