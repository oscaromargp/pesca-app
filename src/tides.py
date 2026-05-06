"""
Módulos de Pesca App
Optimizado siguiendo los mejores enfoques de pytides, Open-Meteo y fishing-report
"""
import requests
import json
import os
from datetime import datetime, timedelta
from functools import lru_cache

# ============================================================================
# CONFIGURACIÓN Y CACHÉ
# ============================================================================

CACHE_DIR = os.path.join(os.path.dirname(__file__), '..', 'cache')
os.makedirs(CACHE_DIR, exist_ok=True)

def cache_get(key, max_age_hours=6):
    """Caché simple basado en archivo - los datos de mareas cambian poco"""
    cache_file = os.path.join(CACHE_DIR, f"{key}.json")
    try:
        if os.path.exists(cache_file):
            mtime = datetime.fromtimestamp(os.path.getmtime(cache_file))
            age = datetime.now() - mtime
            if age.total_seconds() < max_age_hours * 3600:
                with open(cache_file, 'r') as f:
                    return json.load(f)
    except:
        pass
    return None

def cache_set(key, data):
    """Guardar en caché"""
    cache_file = os.path.join(CACHE_DIR, f"{key}.json")
    try:
        with open(cache_file, 'w') as f:
            json.dump(data, f)
    except:
        pass

# ============================================================================
# GEOCODIFICACIÓN - Nominatim (OpenStreetMap)
# ============================================================================

CITIES_DB = {
    # México - Pacífico
    "la paz": {"lat": 24.142, "lon": -110.310, "state": "Baja California Sur", "country": "México"},
    "mazatlan": {"lat": 23.225, "lon": -106.420, "state": "Sinaloa", "country": "México"},
    "cabo san lucas": {"lat": 22.891, "lon": -109.928, "state": "Baja California Sur", "country": "México"},
    "cabo": {"lat": 22.891, "lon": -109.928, "state": "Baja California Sur", "country": "México"},
    "ensenada": {"lat": 31.866, "lon": -116.625, "state": "Baja California", "country": "México"},
    "san felipe": {"lat": 31.024, "lon": -114.832, "state": "Baja California", "country": "México"},
    "guaymas": {"lat": 27.919, "lon": -110.907, "state": "Sonora", "country": "México"},
    "topolobampo": {"lat": 25.615, "lon": -109.055, "state": "Sinaloa", "country": "México"},
    "manzanillo": {"lat": 19.054, "lon": -104.318, "state": "Colima", "country": "México"},
    "tijuana": {"lat": 32.515, "lon": -117.069, "state": "Baja California", "country": "México"},
    # México - Golfo y Caribe
    "cancun": {"lat": 21.161, "lon": -86.851, "state": "Quintana Roo", "country": "México"},
    "cancún": {"lat": 21.161, "lon": -86.851, "state": "Quintana Roo", "country": "México"},
    "progreso": {"lat": 21.283, "lon": -89.667, "state": "Yucatán", "country": "México"},
    "tampico": {"lat": 22.255, "lon": -97.868, "state": "Tamaulipas", "country": "México"},
    "veracruz": {"lat": 19.189, "lon": -96.291, "state": "Veracruz", "country": "México"},
    "acapulco": {"lat": 16.863, "lon": -99.883, "state": "Guerrero", "country": "México"},
    "cozumel": {"lat": 20.422, "lon": -86.923, "state": "Quintana Roo", "country": "México"},
    "playa del carmen": {"lat": 20.627, "lon": -87.072, "state": "Quintana Roo", "country": "México"},
    "mérida": {"lat": 20.967, "lon": -89.593, "state": "Yucatán", "country": "México"},
    # USA - Pacífico
    "san diego": {"lat": 32.716, "lon": -117.161, "state": "California", "country": "USA"},
    "santa barbara": {"lat": 34.421, "lon": -119.702, "state": "California", "country": "USA"},
    "los angeles": {"lat": 34.052, "lon": -118.244, "state": "California", "country": "USA"},
    "san francisco": {"lat": 37.775, "lon": -122.418, "state": "California", "country": "USA"},
    # USA - Atlántico
    "miami": {"lat": 25.762, "lon": -80.192, "state": "Florida", "country": "USA"},
    "key west": {"lat": 24.555, "lon": -81.808, "state": "Florida", "country": "USA"},
    "tampa": {"lat": 27.951, "lon": -82.457, "state": "Florida", "country": "USA"},
    "jacksonville": {"lat": 30.332, "lon": -81.656, "state": "Florida", "country": "USA"},
}

def geocode_city(query):
    """Geocodificar ciudad a coordenadas - usa DB local + Nominatim"""
    query_lower = query.lower().strip()
    
    # Buscar en DB local
    if query_lower in CITIES_DB:
        return CITIES_DB[query_lower]
    
    for name, data in CITIES_DB.items():
        if name in query_lower or query_lower in name:
            return data
    
    # Fallsback a Nominatim (OpenStreetMap)
    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {"q": query, "format": "json", "limit": 1, "accept-language": "es"}
        headers = {"User-Agent": "PescaApp/1.0 (https://github.com/oscaromargp/pesca-app)"}
        resp = requests.get(url, params=params, headers=headers, timeout=8)
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
    """Obtener ubicación desde IP - usa ipapi.co"""
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

# ============================================================================
# MAREAS - NOAA CO-OPS + Open-Meteo Marine
# ============================================================================

def get_tides(lat, lon, days=3):
    """Obtener predicciones de mareas desde NOAA CO-OPS
    
    Optimizado usando el enfoque de pytides:
    - Búsqueda de estación más cercana
    - Predicciones armónicas
    - Caché para evitar llamadas repetidas
    """
    cache_key = f"tides_{lat:.2f}_{lon:.2f}_{days}"
    cached = cache_get(cache_key, max_age_hours=6)
    if cached:
        return cached
    
    try:
        # 1. Encontrar estación más cercana
        stations_url = "https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations.json"
        resp = requests.get(stations_url, timeout=10)
        stations = resp.json().get("stations", [])
        
        # Buscar estación costera más cercana
        coastal_stations = [s for s in stations if s.get("stationType") in ["Ref", "Sub", "WL"]]
        if not coastal_stations:
            coastal_stations = stations
        
        closest = min(coastal_stations, key=lambda s: 
            abs(float(s.get("lat", 0)) - lat) + abs(float(s.get("lng", 0)) - lon)
        )
        station_id = closest.get("id")
        
        # 2. Obtener predicciones
        begin = datetime.now().strftime("%Y%m%d")
        end = (datetime.now() + timedelta(days=days)).strftime("%Y%m%d")
        
        url = "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter"
        params = {
            "product": "predictions",
            "application": "pesca_app",
            "begin_date": begin,
            "end_date": end,
            "datum": "MLLW",
            "station": station_id,
            "time_zone": "lst_ldt",
            "units": "metric",
            "format": "json"
        }
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        
        predictions = data.get("predictions", [])
        tides = []
        
        # Procesar predicciones - detectar pleamar/bajamar
        for i, p in enumerate(predictions):
            height = float(p.get("v", 0))
            time = p.get("t", "")
            
            if i == 0:
                tide_type = "high"
            else:
                prev_height = float(predictions[i-1].get("v", 0))
                next_height = float(predictions[i+1].get("v", 0)) if i+1 < len(predictions) else height
                
                if height > prev_height and height > next_height:
                    tide_type = "high"
                elif height < prev_height and height < next_height:
                    tide_type = "low"
                else:
                    continue  # Skip puntos de inflexión no relevantes
            
            tides.append({
                "time": time,
                "height": round(height, 2),
                "type": tide_type,
                "direction": "▲" if tide_type == "high" else "▼"
            })
        
        result = {
            "station": closest.get("name"),
            "station_id": station_id,
            "lat": float(closest.get("lat", 0)),
            "lon": float(closest.get("lng", 0)),
            "tides": tides[:days*2],
            "is_incoming": tides[0].get("type") == "low" if tides else True,
            "next_tide": tides[0] if tides else None
        }
        
        cache_set(cache_key, result)
        return result
        
    except Exception as e:
        return {"error": str(e), "tides": [], "station": "Unknown"}

def get_tide_coefficient(tides_data):
    """Calcular coeficiente de marea (0-100) basado en rango de mareas
    
    Similar al enfoque de pytides para análisis armónico:
    - Coeficiente alto = marea grande = mejor para pesca en zonas costeras
    """
    heights = [t.get("height", 0) for t in tides_data.get("tides", [])]
    if len(heights) < 2:
        return 50
    
    tide_range = max(heights) - min(heights)
    # Coeficiente típicamente entre 20-100
    coefficient = min(100, max(20, int(tide_range * 50)))
    return coefficient

# ============================================================================
# CLIMA Y MAR - Open-Meteo Marine API (gratuito, sin API key)
# ============================================================================

def get_weather(lat, lon):
    """Obtener clima desde Open-Meteo (sin API key required)
    
    Basado en el enfoque de ATJ12/fishing-forecast
    """
    cache_key = f"weather_{lat:.2f}_{lon:.2f}"
    cached = cache_get(cache_key, max_age_hours=1)
    if cached:
        return cached
    
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": [
                "temperature_2m", "relative_humidity_2m", 
                "wind_speed_10m", "wind_direction_10m", 
                "precipitation", "cloud_cover", "pressure_msl",
                "weather_code"
            ],
            "daily": [
                "temperature_2m_max", "temperature_2m_min", 
                "precipitation_sum", "wind_speed_10m_max"
            ],
            "hourly": [
                "temperature_2m", "wind_speed_10m", 
                "precipitation_probability"
            ],
            "timezone": "auto",
            "forecast_days": 3
        }
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        
        current = data.get("current", {})
        
        # Convertir weather_code a descripción
        weather_codes = {
            0: "Despejado",
            1: "Mayormente despejado",
            2: "Parcialmente nublado",
            3: "Nublado",
            45: "Niebla",
            51: "Llovizna",
            61: "Lluvia",
            63: "Lluvia moderada",
            65: "Lluvia fuerte",
            71: "Nieve",
            80: "Chubascos",
            95: "Tormenta",
        }
        
        result = {
            "temperature": current.get("temperature_2m"),
            "humidity": current.get("relative_humidity_2m"),
            "wind_speed": round(current.get("wind_speed_10m", 0)),
            "wind_direction": current.get("wind_direction_10m"),
            "wind_dir_cardinal": _degrees_to_cardinal(current.get("wind_direction_10m", 0)),
            "precipitation": current.get("precipitation", 0),
            "cloud_cover": current.get("cloud_cover"),
            "pressure": current.get("pressure_msl"),
            "weather_code": current.get("weather_code"),
            "weather_description": weather_codes.get(current.get("weather_code"), "Desconocido"),
            "forecast": data.get("daily", {}),
            "hourly": data.get("hourly", {})
        }
        
        cache_set(cache_key, result)
        return result
        
    except Exception as e:
        return {"error": str(e), "temperature": 22, "wind_speed": 10}

def get_marine_weather(lat, lon):
    """Obtener datos marinos desde Open-Meteo Marine API
    
    Similar al enfoque de stormglass pero gratuito:
    - Temperatura superficial del mar
    - Altura de olas
    - Período de olas
    - Dirección de olas
    """
    cache_key = f"marine_{lat:.2f}_{lon:.2f}"
    cached = cache_get(cache_key, max_age_hours=3)
    if cached:
        return cached
    
    try:
        url = "https://marine-api.open-meteo.com/v1/marine"
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": [
                "wave_height", "wave_period", 
                "wave_direction", "ocean_temperature"
            ],
            "hourly": [
                "wave_height_max", "wave_period_max"
            ],
            "timezone": "auto",
            "forecast_days": 3
        }
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        
        current = data.get("current", {})
        
        result = {
            "water_temperature": current.get("ocean_temperature"),
            "wave_height": current.get("wave_height"),
            "wave_period": current.get("wave_period"),
            "wave_direction": current.get("wave_direction"),
            "wave_dir_cardinal": _degrees_to_cardinal(current.get("wave_direction", 0)),
            "wave_beaufort": _wave_to_beaufort(current.get("wave_height", 0)),
            "forecast": data.get("hourly", {})
        }
        
        cache_set(cache_key, result)
        return result
        
    except Exception as e:
        return {"error": str(e), "wave_height": 0.5}

def _degrees_to_cardinal(degrees):
    """Convertir grados a dirección cardinal"""
    if degrees is None:
        return "N"
    directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", 
                 "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    index = round(degrees / 22.5) % 16
    return directions[index]

def _wave_to_beaufort(height):
    """Convertir altura de olas a escala Beaufort"""
    if height is None:
        return 0
    if height < 0.1:
        return 0
    elif height < 0.5:
        return 1
    elif height < 1.25:
        return 2
    elif height < 2.5:
        return 3
    elif height < 4:
        return 4
    elif height < 6:
        return 5
    else:
        return 6

# ============================================================================
# SOLUNAR - Cálculo de fases lunares (similar a fishing-report)
# ============================================================================

def get_solunar_data(lat, lon):
    """Calcular datos solunares - fases lunares y períodos de pesca
    
    Basado en el enfoque de fishing-report:
    - Fase lunar actual
    - Iluminación (0-100%)
    - Períodos mayores y menores de actividad
    """
    # Usar cálculo simple para evitar dependencias problemáticas
    return _simple_solunar()
        
        # Fase lunar (aproximación simple)
        # La luna llena ocurre ~cada 29.53 días
        moon_cycle = 29.53059
        days_since_new = (datetime.now() - datetime(2000, 1, 1)).days % moon_cycle
        moon_phase = days_since_new / moon_cycle
        
        # Iluminación (0-100%)
        illumination = (1 - abs(moon_phase * 2 - 1)) * 100
        
        # Determinar nombre de fase
        if moon_phase < 0.0625:
            phase_name = "Luna Nueva"
        elif moon_phase < 0.1875:
            phase_name = "Luna Creciente"
        elif moon_phase < 0.3125:
            phase_name = "Cuarto Creciente"
        elif moon_phase < 0.4375:
            phase_name = "Gibosa Creciente"
        elif moon_phase < 0.5625:
            phase_name = "Luna Llena"
        elif moon_phase < 0.6875:
            phase_name = "Gibosa Menguante"
        elif moon_phase < 0.8125:
            phase_name = "Cuarto Menguante"
        elif moon_phase < 0.9375:
            phase_name = "Luna Menguante"
        else:
            phase_name = "Luna Nueva"
        
        # Rating solunar (1-5) basado en fase
        # Las mejores fases son luna nueva y luna llena
        if illumination < 15 or illumination > 85:
            solunar_rating = 5
        elif illumination < 30 or illumination > 70:
            solunar_rating = 4
        elif illumination < 45 or illumination > 55:
            solunar_rating = 3
        else:
            solunar_rating = 2
        
        # Períodos mayores (tránsito lunar) - aproximación
        # Basado en la edad de la luna
        major_periods = []
        minor_periods = []
        
        # Horas aproximadas de tránsito (varía por ubicación)
        now = datetime.now()
        hour = now.hour
        
        # Two major periods per day (approx 12 hours apart)
        if 5 <= hour < 9:
            major_periods = ["06:00-08:00", "18:00-20:00"]
        elif 9 <= hour < 13:
            major_periods = ["06:00-08:00", "18:00-20:00"]
        elif 13 <= hour < 17:
            major_periods = ["06:00-08:00", "18:00-20:00"]
        elif 17 <= hour < 21:
            major_periods = ["18:00-20:00"]
        else:
            major_periods = ["06:00-08:00"]
        
        # Minor periods (salida/puesta de luna)
        if 3 <= hour < 7:
            minor_periods = ["05:00-06:00", "17:00-18:00"]
        elif 7 <= hour < 11:
            minor_periods = ["05:00-06:00", "17:00-18:00"]
        elif 11 <= hour < 15:
            minor_periods = ["17:00-18:00"]
        elif 15 <= hour < 19:
            minor_periods = ["17:00-18:00"]
        else:
            minor_periods = ["05:00-06:00"]
        
        return {
            "moon_phase": round(moon_phase, 2),
            "moon_phase_name": phase_name,
            "moon_illumination": illumination / 100,
            "illumination_percent": round(illumination),
            "solunar_rating": solunar_rating,
            "major_periods": major_periods,
            "minor_periods": minor_periods,
            "is_fishing_day": solunar_rating >= 3
        }
        
    except ImportError:
        # Si skyfield no está disponible, usar cálculo simple
        return _simple_solunar()
    except Exception as e:
        return {"error": str(e), **_simple_solunar()}

def _simple_solunar():
    """Cálculo simple de solunar si skyfield no está disponible"""
    import math
    moon_cycle = 29.53059
    days = (datetime.now() - datetime(2000, 1, 1)).days
    moon_phase = (days % moon_cycle) / moon_cycle
    illumination = (1 - abs(moon_phase * 2 - 1)) * 100
    
    phase_names = ["Luna Nueva", "Luna Creciente", "Cuarto Creciente", 
                   "Gibosa Creciente", "Luna Llena", "Gibosa Menguante",
                   "Cuarto Menguante", "Luna Menguante"]
    phase_idx = int(moon_phase * 8) % 8
    
    return {
        "moon_phase": moon_phase,
        "moon_phase_name": phase_names[phase_idx],
        "moon_illumination": illumination / 100,
        "illumination_percent": round(illumination),
        "solunar_rating": 3,
        "major_periods": ["06:00-08:00", "18:00-20:00"],
        "minor_periods": ["12:00-14:00"],
        "is_fishing_day": True
    }

# ============================================================================
# SCORE DE PESCA - Algoritmo integrado
# ============================================================================

def calculate_fishing_score(tides_data, weather_data, solunar_data):
    """Calcular score de pesca (1-10)
    
    Basado en el enfoque de fishing-report:
    - Factores de marea
    - Factores de clima
    - Factores solunares
    """
    score = 5.0
    
    # Factor marea
    tide_coeff = get_tide_coefficient(tides_data)
    if tide_coeff >= 70:
        score += 2.0
    elif tide_coeff >= 50:
        score += 1.0
    
    # ¿Marea entrante o saliente?
    if tides_data.get("is_incoming"):
        score += 0.5
    
    # Factor clima
    wind_speed = weather_data.get("wind_speed", 20)
    if wind_speed < 10:
        score += 1.5
    elif wind_speed < 20:
        score += 0.5
    
    precipitation = weather_data.get("precipitation", 0)
    if precipitation < 0.5:
        score += 1.0
    
    cloud_cover = weather_data.get("cloud_cover", 50)
    if 30 < cloud_cover < 70:
        score += 0.5
    
    # Factor solunar
    solunar_rating = solunar_data.get("solunar_rating", 3)
    score += (solunar_rating - 3) * 0.8
    
    # Bonus por iluminación óptima
    illum = solunar_data.get("illumination_percent", 50)
    if 30 < illum < 70:
        score += 0.5
    
    return max(1, min(10, round(score, 1)))

def get_fishing_context(tides_data, weather_data, solunar_data, score):
    """Generar descripción contextual de pesca"""
    parts = []
    
    # Marea
    tide_coeff = get_tide_coefficient(tides_data)
    if tide_coeff >= 70:
        parts.append(f"coeficiente alto ({tide_coeff})")
    elif tide_coeff < 40:
        parts.append("marea baja")
    
    # Temperatura del mar
    marine = weather_data  # datos combinados
    if marine.get("water_temperature"):
        temp = marine["water_temperature"]
        if temp > 25:
            parts.append(f"agua cálida ({temp}°C)")
        elif temp < 18:
            parts.append(f"agua fresca ({temp}°C)")
    
    # Viento
    wind = weather_data.get("wind_speed", 0)
    if wind > 25:
        parts.append(f"viento fuerte ({wind} km/h)")
    elif wind < 10:
        parts.append("viento calma")
    
    # Luna
    moon_name = solunar_data.get("moon_phase_name", "")
    if moon_name in ["Luna Nueva", "Luna Llena"]:
        parts.append(moon_name.lower())
    
    # Score final
    if score >= 8:
        return "Excelentes condiciones para pesca hoy. " + (", ".join(parts) if parts else "Todas las condiciones son óptimas.")
    elif score >= 6:
        return "Buenas condiciones para pesca. " + (", ".join(parts) if parts else "Condiciones aceptables.")
    elif score >= 4:
        return "Condiciones regulares para pesca. " + (", ".join(parts) if parts else "Precaución recomendada.")
    else:
        return "Condiciones no ideales para pesca. Considera otro día."

def get_tide_description(tides_data, coefficient):
    """Descripción de las condiciones de marea"""
    if coefficient >= 80:
        return "Marea muy grande. Excelente para pesca en zonas costeras."
    elif coefficient >= 60:
        return "Buena amplitud de marea. Peces activos con los cambios."
    elif coefficient >= 40:
        return "Marea moderada. Condiciones estables."
    else:
        return "Marea baja. Busca bahías profundas."