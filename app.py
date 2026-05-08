"""
Pesca App - Backend
Optimizado: Flask + Open-Meteo + NOAA + Skyfield
Server-Side Rendering para mejor rendimiento y SEO
"""
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import os
import json

port = int(os.environ.get('PORT', 5000))

app = Flask(__name__, static_folder='static', template_folder='static')
CORS(app)

from src.tides import (
    get_tides, get_weather, get_marine_weather, get_solunar_data,
    calculate_fishing_score, get_fishing_context, get_tide_coefficient,
    geocode_city, get_location_from_ip
)

@app.route('/')
def index():
    """Página principal con datos precargados (Server-Side Rendering)"""
    # Obtener ubicación del query o usar默认值
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    city = request.args.get('city')
    
    if city:
        result = geocode_city(city)
        if result:
            lat = result.get("lat")
            lon = result.get("lon")
    
    if lat is None or lon is None:
        lat = 24.142
        lon = -110.310
    
    # Obtener datos para la ubicación
    tides_data = get_tides(lat, lon)
    weather_data = get_weather(lat, lon)
    marine_data = get_marine_weather(lat, lon)
    solunar_data = {"moon_phase_name": "Luna Creciente", "illumination_percent": 50, "solunar_rating": 3}
    
    tide_coefficient = get_tide_coefficient(tides_data)
    fishing_score = calculate_fishing_score(tides_data, weather_data, solunar_data)
    weather_data.update(marine_data)
    
    city_name = city or "La Paz"
    country = "México"
    
    # Datos precargados para el template
    forecast_data = {
        "location": {"lat": lat, "lon": lon, "city": city_name, "country": country},
        "fishing_score": fishing_score,
        "fishing_context": f"Score: {fishing_score}/10 - Condiciones de pesca en {city_name}",
        "tide_coefficient": tide_coefficient,
        "tides": tides_data,
        "weather": weather_data,
        "solunar": solunar_data
    }
    
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
    """Pronóstico completo de pesca"""
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    city = request.args.get('city')
    
    # Resolver ubicación
    if city:
        result = geocode_city(city)
        if result:
            lat = result.get("lat")
            lon = result.get("lon")
    
    if lat is None or lon is None:
        lat = 24.142
        lon = -110.310
    
    # Default city
    city_name = city or "La Paz"
    country = "México"
    
    # Obtener datos
    tides_data = get_tides(lat, lon)
    weather_data = get_weather(lat, lon)
    marine_data = get_marine_weather(lat, lon)
    solunar_data = {"moon_phase_name": "Luna Creciente", "illumination_percent": 50, "solunar_rating": 3}
    
    # Calcular scores
    tide_coefficient = get_tide_coefficient(tides_data)
    fishing_score = calculate_fishing_score(tides_data, weather_data, solunar_data)
    weather_data.update(marine_data)
    
    return jsonify({
        "location": {"lat": lat, "lon": lon, "city": city_name, "country": country},
        "fishing_score": fishing_score,
        "fishing_context": f"Score: {fishing_score}/10 - Condiciones de pesca en {city_name}",
        "tide_coefficient": tide_coefficient,
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
        try:
            location = get_location_from_ip()
            lat = location.get("lat") or 24.142
            lon = location.get("lon") or -110.310
        except:
            lat = 24.142
            lon = -110.310
    
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
        try:
            location = get_location_from_ip()
            lat = location.get("lat") or 24.142
            lon = location.get("lon") or -110.310
        except:
            lat = 24.142
            lon = -110.310
    
    weather = get_weather(lat, lon)
    weather.update(get_marine_weather(lat, lon))
    return jsonify(weather)

@app.route('/api/solunar')
def solunar():
    """Solo datos solunares
    
    Uso: /api/solunar?lat=24.142&lon=-110.310
    """
    lat = request.args.get('lat', type=float) or 24.142
    lon = request.args.get('lon', type=float) or -110.310
    
    try:
        return jsonify(get_solunar_data(lat, lon))
    except Exception as e:
        return jsonify({"error": str(e), "moon_phase_name": "Error"})

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

@app.route('/api/fish-guide')
def fish_guide():
    """Guía completa de pesca para la ubicación
    
    Uso: /api/fish-guide?lat=24.142&lon=-110.310&city=La+Paz
    Devuelve: Especies recomendadas, técnicas, señuelos, carnadas, horarios óptimos
    """
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    city = request.args.get('city')
    
    # Resolver ubicación
    if city:
        result = geocode_city(city)
        if result:
            lat = result.get("lat")
            lon = result.get("lon")
    
    if lat is None or lon is None:
        lat = 24.142
        lon = -110.310
    
    city_name = city or "La Paz"
    
    # Obtener datos
    tides_data = get_tides(lat, lon)
    weather_data = get_weather(lat, lon)
    weather_data.update(get_marine_weather(lat, lon))
    
    # Generar guía
    try:
        from src.recommendations import generate_fishing_guide
        guide = generate_fishing_guide(lat, lon, weather_data, tides_data, city_name)
        return jsonify(guide)
    except Exception as e:
        return jsonify({"error": str(e), "location": city_name})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=False)