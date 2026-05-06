from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from src.utils import get_location_from_ip, calculate_fishing_score
from src.tides import get_tides
from src.weather import get_weather, get_marine_weather
from src.solunar import get_solunar_data
import os

app = Flask(__name__, static_folder='static', template_folder='static')
CORS(app)

# Get port from environment or default to 10000
port = int(os.environ.get('PORT', 10000))

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/forecast')
def forecast():
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    ip = request.args.get('ip')
    
    # Get location from IP if no coordinates
    if lat is None or lon is None:
        location = get_location_from_ip(ip)
        lat = location.get("lat")
        lon = location.get("lon")
    else:
        location = get_location_from_ip()
    
    # Get all data
    tides_data = get_tides(lat, lon)
    weather_data = get_weather(lat, lon)
    marine_data = get_marine_weather(lat, lon)
    solunar_data = get_solunar_data(lat, lon)
    
    # Calculate fishing score
    fishing_score = calculate_fishing_score(tides_data, weather_data, solunar_data)
    
    return jsonify({
        "location": {
            "lat": lat,
            "lon": lon,
            "city": location.get("city"),
            "country": location.get("country")
        },
        "fishing_score": fishing_score,
        "tides": tides_data,
        "weather": weather_data,
        "marine": marine_data,
        "solunar": solunar_data
    })

@app.route('/api/tides')
def tides():
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    if lat is None or lon is None:
        location = get_location_from_ip()
        lat, lon = location.get("lat"), location.get("lon")
    return jsonify(get_tides(lat, lon))

@app.route('/api/weather')
def weather():
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    if lat is None or lon is None:
        location = get_location_from_ip()
        lat, lon = location.get("lat"), location.get("lon")
    return jsonify(get_weather(lat, lon))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=False)
