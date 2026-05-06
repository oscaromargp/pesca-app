"""
Pesca App - Backend
Optimizado: Flask + Open-Meteo + NOAA + Skyfield
"""
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import os

# Render asigna el puerto automáticamente
port = int(os.environ.get('PORT', 5000))

app = Flask(__name__, static_folder='static', template_folder='static')
CORS(app)

# Importar módulos optimizados
from src.tides import (
    get_tides, get_weather, get_marine_weather, get_solunar_data,
    calculate_fishing_score, get_fishing_context, get_tide_coefficient,
    geocode_city, get_location_from_ip
)

@app.route('/')
def index():
    """Página principal"""
    return app.send_static_file('index.html')

@app.route('/api/geocode')
def geocode():
    """Geocodificar ciudad a coordenadas
    
    Uso: /api/geocode?q=La+Paz
    """
    query = request.args.get('q', '')
    if not query:
        return jsonify({"error": "Falta parámetro 'q'"}), 400
    
    result = geocode_city(query)
    if result:
        return jsonify(result)
    return jsonify({"error": "Ubicación no encontrada"}), 404

@app.route('/api/forecast')
def forecast():
    """Pronóstico completo de pesca
    
    Parámetros:
    - lat, lon: coordenadas (opcional)
    - city: nombre de ciudad (opcional, prioriza sobre lat/lon)
    - ip: usar IP del cliente (opcional)
    
    Uso: 
    - /api/forecast?lat=24.142&lon=-110.310
    - /api/forecast?city=La+Paz
    - /api/forecast (usa IP)
    """
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    city = request.args.get('city')
    ip = request.args.get('ip')
    
    # 1. Resolver ubicación
    if city:
        result = geocode_city(city)
        if result:
            lat = result.get("lat")
            lon = result.get("lon")
    
    if lat is None or lon is None:
        location = get_location_from_ip(ip)
        lat = location.get("lat")
        lon = location.get("lon")
    
    # 2. Obtener todos los datos
    tides_data = get_tides(lat, lon)
    weather_data = get_weather(lat, lon)
    marine_data = get_marine_weather(lat, lon)
    solunar_data = get_solunar_data(lat, lon)
    
    # 3. Calcular scores
    tide_coefficient = get_tide_coefficient(tides_data)
    fishing_score = calculate_fishing_score(tides_data, weather_data, solunar_data)
    tide_description = get_tide_description(tides_data, tide_coefficient)
    fishing_context = get_fishing_context(tides_data, marine_data, solunar_data, fishing_score)
    
    # 4. Combinar datos del clima
    weather_data.update(marine_data)
    
    # 5. Obtener nombre de ubicación
    ip_location = get_location_from_ip()
    city_name = city or ip_location.get("city", "Unknown")
    
    return jsonify({
        "location": {
            "lat": lat,
            "lon": lon,
            "city": city_name,
            "country": ip_location.get("country", "Unknown")
        },
        "fishing_score": fishing_score,
        "fishing_context": fishing_context,
        "tide_coefficient": tide_coefficient,
        "tide_description": tide_description,
        "tides": tides_data,
        "weather": weather_data,
        "solunar": solunar_data
    })

@app.route('/api/tides')
def tides():
    """Solo datos de mareas
    
    Uso: /api/tides?lat=24.142&lon=-110.310
    """
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    city = request.args.get('city')
    days = request.args.get('days', 3, type=int)
    
    if city:
        result = geocode_city(city)
        if result:
            lat = result.get("lat")
            lon = result.get("lon")
    
    if lat is None or lon is None:
        location = get_location_from_ip()
        lat, lon = location.get("lat"), location.get("lon")
    
    return jsonify(get_tides(lat, lon, days))

@app.route('/api/weather')
def weather():
    """Solo datos de clima y marino
    
    Uso: /api/weather?lat=24.142&lon=-110.310
    """
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
    weather.update(get_marine_weather(lat, lon))
    return jsonify(weather)

@app.route('/api/solunar')
def solunar():
    """Solo datos solunares
    
    Uso: /api/solunar?lat=24.142&lon=-110.310
    """
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    
    return jsonify(get_solunar_data(lat, lon))

@app.route('/api/search')
def search():
    """Búsqueda de ubicaciones populares
    
    Uso: /api/search?q=Maz
    Devuelve: lista de ciudades que coinciden
    """
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify([])
    
    from src.tides import CITIES_DB
    matches = [
        {"name": name.title(), "lat": data["lat"], "lon": data["lon"], 
         "state": data.get("state", ""), "country": data.get("country", "")}
        for name, data in CITIES_DB.items()
        if query in name
    ]
    return jsonify(matches)

@app.route('/health')
def health():
    """Health check para monitoring"""
    return jsonify({"status": "ok", "app": "pesca-app"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=False)