from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from src.utils import get_location_from_ip, calculate_fishing_score, geocode_city, calculate_tide_coefficient, get_tide_description, get_fishing_context
from src.tides import get_tides
from src.weather import get_weather, get_marine_weather
from src.solunar import get_solunar_data
import os

app = Flask(__name__, static_folder='static', template_folder='static')
CORS(app)

port = int(os.environ.get('PORT', 5000))

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/geocode')
def geocode():
    """Resolve city name to coordinates"""
    query = request.args.get('q', '')
    if not query:
        return jsonify({"error": "Missing query parameter 'q'"}), 400
    
    result = geocode_city(query)
    if result:
        return jsonify(result)
    return jsonify({"error": "Location not found"}), 404

@app.route('/api/forecast')
def forecast():
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    city = request.args.get('city')
    ip = request.args.get('ip')
    
    if city:
        result = geocode_city(city)
        if result:
            lat = result.get("lat")
            lon = result.get("lon")
    
    if lat is None or lon is None:
        location = get_location_from_ip(ip)
        lat = location.get("lat")
        lon = location.get("lon")
    else:
        location = {"lat": lat, "lon": lon}
    
    tides_data = get_tides(lat, lon)
    weather_data = get_weather(lat, lon)
    marine_data = get_marine_weather(lat, lon)
    solunar_data = get_solunar_data(lat, lon)
    
    tide_coefficient = calculate_tide_coefficient(tides_data)
    fishing_score = calculate_fishing_score(tides_data, weather_data, solunar_data)
    tide_description = get_tide_description(tides_data, tide_coefficient)
    fishing_context = get_fishing_context(tides_data, weather_data, solunar_data, fishing_score)
    
    ip_location = get_location_from_ip()
    city_name = location.get("city") or ip_location.get("city", "Unknown")
    country = location.get("country") or ip_location.get("country", "Unknown")
    
    return jsonify({
        "location": {
            "lat": lat,
            "lon": lon,
            "city": city_name,
            "country": country
        },
        "fishing_score": fishing_score,
        "fishing_context": fishing_context,
        "tide_description": tide_description,
        "tide_coefficient": tide_coefficient,
        "tides": tides_data,
        "weather": weather_data,
        "marine": marine_data,
        "solunar": solunar_data
    })

@app.route('/api/tides')
def tides():
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    city = request.args.get('city')
    
    if city:
        result = geocode_city(city)
        if result:
            lat = result.get("lat")
            lon = result.get("lon")
    
    if lat is None or lon is None:
        location = get_location_from_ip()
        lat, lon = location.get("lat"), location.get("lon")
    
    return jsonify(get_tides(lat, lon))

@app.route('/api/weather')
def weather():
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    city = request.args.get('city')
    
    if city:
        result = geocode_city(city)
        if result:
            lat = result.get("lat")
            lon = result.get("lon")
    
    if lat is None or lon is None:
        location = get_location_from_ip()
        lat, lon = location.get("lat"), location.get("lon")
    
    weather = get_weather(lat, lon)
    marine = get_marine_weather(lat, lon)
    weather.update(marine)
    return jsonify(weather)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=False)