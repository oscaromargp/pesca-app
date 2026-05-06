import requests
from datetime import datetime, timedelta

CITIES_DB = {
    "la paz": {"lat": 24.142, "lon": -110.310, "state": "Baja California Sur", "country": "México"},
    "mazatlán": {"lat": 23.225, "lon": -106.420, "state": "Sinaloa", "country": "México"},
    "cabo san lucas": {"lat": 22.891, "lon": -109.928, "state": "Baja California Sur", "country": "México"},
    "ensenada": {"lat": 31.866, "lon": -116.625, "state": "Baja California", "country": "México"},
    "san felipe": {"lat": 31.024, "lon": -114.832, "state": "Baja California", "country": "México"},
    "guaymas": {"lat": 27.919, "lon": -110.907, "state": "Sonora", "country": "México"},
    "topolobampo": {"lat": 25.615, "lon": -109.055, "state": "Sinaloa", "country": "México"},
    "manzanillo": {"lat": 19.054, "lon": -104.318, "state": "Colima", "country": "México"},
    "cancelún": {"lat": 18.653, "lon": -91.477, "state": "Campeche", "country": "México"},
    "progreso": {"lat": 21.283, "lon": -89.667, "state": "Yucatán", "country": "México"},
    "tampico": {"lat": 22.255, "lon": -97.868, "state": "Tamaulipas", "country": "México"},
    "veracruz": {"lat": 19.189, "lon": -96.291, "state": "Veracruz", "country": "México"},
    "miami": {"lat": 25.762, "lon": -80.192, "state": "Florida", "country": "USA"},
    "key west": {"lat": 24.555, "lon": -81.808, "state": "Florida", "country": "USA"},
    "santa barbara": {"lat": 34.421, "lon": -119.702, "state": "California", "country": "USA"},
    "san diego": {"lat": 32.716, "lon": -117.161, "state": "California", "country": "USA"},
}

def geocode_city(query):
    """Geocode city name to lat/lon using Nominatim (free)"""
    query_lower = query.lower().strip()
    
    if query_lower in CITIES_DB:
        return CITIES_DB[query_lower]
    
    for name, data in CITIES_DB.items():
        if name in query_lower or query_lower in name:
            return data
    
    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {"q": query, "format": "json", "limit": 1, "accept-language": "es"}
        resp = requests.get(url, params=params, timeout=8, headers={"User-Agent": "PescaApp/1.0"})
        data = resp.json()
        if data:
            return {
                "lat": float(data[0]["lat"]),
                "lon": float(data[0]["lon"]),
                "city": data[0].get("display_name", query).split(",")[0],
                "country": data[0].get("display_name", "").split(",")[-1].strip()
            }
    except:
        pass
    
    return None

def get_location_from_ip(ip=None):
    """Get location from IP address"""
    try:
        url = f"https://ipapi.co/{ip if ip else ''}/json/"
        resp = requests.get(url, timeout=5)
        data = resp.json()
        return {
            "lat": data.get("latitude"),
            "lon": data.get("longitude"),
            "city": data.get("city"),
            "country": data.get("country_name"),
            "region": data.get("region"),
            "ip": data.get("ip")
        }
    except:
        return {"lat": 24.142, "lon": -110.310, "city": "La Paz", "country": "México", "region": "Baja California Sur"}

def calculate_tide_coefficient(tide_data):
    """Calculate tide coefficient (0-100) based on tide range"""
    heights = [t.get("height", 0) for t in tide_data.get("tides", [])]
    if len(heights) < 2:
        return 50
    
    tide_range = max(heights) - min(heights)
    coefficient = min(100, int(tide_range * 50))
    return coefficient

def calculate_fishing_score(tide_data, weather_data, solunar_data):
    """Calculate fishing score 1-10 based on multiple factors"""
    score = 5.0
    
    tide_coeff = calculate_tide_coefficient(tide_data)
    if tide_coeff >= 70:
        score += 2.0
    elif tide_coeff >= 50:
        score += 1.0
    
    heights = [t.get("height", 0) for t in tide_data.get("tides", [])]
    if heights and heights[0] < 0.5:
        score += 0.5
    
    wind_speed = weather_data.get("wind_speed", 20)
    if wind_speed < 10:
        score += 1.5
    elif wind_speed < 20:
        score += 0.5
    
    if weather_data.get("precipitation", 1) < 0.5:
        score += 1.0
    
    cloud_cover = weather_data.get("cloud_cover", 50)
    if 30 < cloud_cover < 70:
        score += 0.5
    
    solunar_rating = solunar_data.get("solunar_rating", 3)
    score += (solunar_rating - 3) * 0.8
    
    moon_illumination = solunar_data.get("moon_illumination", 0.5)
    if 0.4 < moon_illumination < 0.6:
        score += 0.5
    
    return max(1, min(10, round(score, 1)))

def get_tide_description(tide_data, coefficient):
    """Get contextual description of tide conditions"""
    if coefficient >= 80:
        return "Marea muy grande (coeficiente alto). Excelente para pesca en zonas costeras."
    elif coefficient >= 60:
        return "Buena amplitud de marea. Movimientos de peces activos."
    elif coefficient >= 40:
        return "Marea moderada. Condiciones estables para pesca."
    else:
        return "Marea baja. Mejor buscar bahas profundas."

def get_fishing_context(tide_data, weather_data, solunar_data, score):
    """Generate contextual fishing description"""
    parts = []
    
    tide_coeff = calculate_tide_coefficient(tide_data)
    if tide_coeff >= 70:
        parts.append(f"coeficiente de marea alto ({tide_coeff})")
    
    water_temp = weather_data.get("water_temperature")
    if water_temp:
        if water_temp > 25:
            parts.append(f"agua cálida ({water_temp}°C)")
        elif water_temp < 20:
            parts.append(f"agua fresca ({water_temp}°C)")
    
    moon = solunar_data.get("moon_illumination", 0) * 100
    if moon > 70:
        parts.append("luna llena")
    elif moon < 20:
        parts.append("luna nueva")
    
    wind = weather_data.get("wind_speed", 0)
    if wind > 25:
        parts.append(f"viento fuerte ({wind} km/h)")
    elif wind < 10:
        parts.append("viento calma")
    
    if score >= 8:
        return "Excelentes condiciones para pesca hoy. " + ", ".join(parts) if parts else "Todas las condiciones son óptimas."
    elif score >= 6:
        return "Buenas condiciones para pesca. " + ", ".join(parts) if parts else "Condiciones aceptables."
    elif score >= 4:
        return "Condiciones regulares. " + ", ".join(parts) if parts else "Precaución recomendada."
    else:
        return "Condiciones no ideales. Considera otro día."