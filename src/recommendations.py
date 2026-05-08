"""
Fish Recommendations Engine
Recomienda especies y lugares alternativos basados en ubicación, condiciones y temporada
"""
import random
from datetime import datetime, timedelta
import math

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calcula distancia en km entre dos puntos"""
    R = 6371  # Radio de la Tierra en km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def get_distance_text(km):
    """Formatea distancia"""
    if km < 1:
        return f"{int(km*1000)} m"
    elif km < 100:
        return f"{int(km)} km"
    else:
        return f"{int(km)} km"

# base de datos de ubicaciones de pesca principales con scores típicos
FISHING_LOCATIONS = {
    "la paz": {"lat": 24.142, "lon": -110.310, "name": "La Paz", "state": "Baja California Sur", "typical_score": 75},
    "cabo san lucas": {"lat": 22.891, "lon": -109.928, "name": "Cabo San Lucas", "state": "Baja California Sur", "typical_score": 85},
    "cabo": {"lat": 22.891, "lon": -109.928, "name": "Cabo San Lucas", "state": "Baja California Sur", "typical_score": 85},
    "mazatlan": {"lat": 23.225, "lon": -106.420, "name": "Mazatlán", "state": "Sinaloa", "typical_score": 70},
    "ensenada": {"lat": 31.866, "lon": -116.625, "name": "Ensenada", "state": "Baja California", "typical_score": 65},
    "san felipe": {"lat": 31.024, "lon": -114.832, "name": "San Felipe", "state": "Baja California", "typical_score": 60},
    "guaymas": {"lat": 27.919, "lon": -110.907, "name": "Guaymas", "state": "Sonora", "typical_score": 65},
    "topolobampo": {"lat": 25.615, "lon": -109.055, "name": "Topolobampo", "state": "Sinaloa", "typical_score": 70},
    "manzanillo": {"lat": 19.054, "lon": -104.318, "name": "Manzanillo", "state": "Colima", "typical_score": 65},
    "san diego": {"lat": 32.716, "lon": -117.161, "name": "San Diego", "state": "California", "country": "USA", "typical_score": 60},
    "miami": {"lat": 25.762, "lon": -80.192, "name": "Miami", "state": "Florida", "country": "USA", "typical_score": 55},
    "key west": {"lat": 24.555, "lon": -81.808, "name": "Key West", "state": "Florida", "country": "USA", "typical_score": 70},
}

def find_alternative_locations(lat, lon, weather, max_distance_km=100):
    """Encuentra ubicaciones alternativas con mejores condiciones"""
    alternatives = []
    
    # Evaluar cada ubicación conocida
    for loc_id, loc_data in FISHING_LOCATIONS.items():
        dist = calculate_distance(lat, lon, loc_data["lat"], loc_data["lon"])
        
        # Solo considerar dentro del radio
        if dist <= max_distance_km and dist > 0:
            # Calcular score basado en condiciones actuales
            score = loc_data.get("typical_score", 50)
            
            # Ajustar por condición actual
            temp = weather.get("temperature", 22)
            wind = weather.get("wind_speed", 10)
            
            # Reducir si mucha calor o mucho viento
            if temp > 30:
                score -= 10
            elif temp < 18:
                score -= 5
            
            if wind > 30:
                score -= 15
            elif wind > 20:
                score -= 10
            
            score = max(0, min(100, score))
            
            alternatives.append({
                "id": loc_id,
                "name": loc_data["name"],
                "state": loc_data.get("state", ""),
                "distance": dist,
                "distance_text": get_distance_text(dist),
                "lat": loc_data["lat"],
                "lon": loc_data["lon"],
                "score": score,
                "reason": get_alternative_reason(loc_id, score, temp, wind)
            })
    
    # Ordenar por score descendente
    alternatives.sort(key=lambda x: x["score"], reverse=True)
    
    return alternatives[:4]  # Top 4 alternativas

def get_season_score(month, lat):
    """Score de temporada para el mes actual"""
    # Temporada de peces en el Pacífico mexicano
    season_data = {
        "dorado": {    "peak": [6, 7, 8, 9, 10],  # Julio-Nov
            "good": [5, 11]},
        "marlin_negro": {    "peak": [7, 8, 9, 10],   # Agosto-Oct
            "good": [6, 11]},
        "marlin_azul": {    "peak": [7, 8, 9, 10],
            "good": [6, 11]},
        "sailfish": {    "peak": [12, 1, 2, 3],  # Enero-Marzo
            "good": [11, 4]},
        "cabrilla": {    "peak": range(1, 13),  # Todo el año
            "good": []},
        "lubina": {    "peak": [3, 4, 5, 9, 10, 11],
            "good": [2, 6, 7, 8]},
        "pargo": {    "peak": [3, 4, 5, 6, 7, 8, 9, 10],
            "good": [2, 11, 12]},
        "huachinango": {    "peak": range(1, 13),
            "good": []},
        "tuna": {    "peak": [4, 5, 6, 7, 8, 9, 10],
            "good": [3, 11]},
        "bonito": {    "peak": [3, 4, 5, 6, 10, 11],
            "good": [2, 7, 8, 9]},
        "wahoo": {    "peak": [3, 4, 5, 6],
            "good": [2, 7]},
        "mackerel": {    "peak": [1, 2, 3, 4],
            "good": [12]},
        "trucha": {    "peak": [1, 2, 3, 4, 11, 12],
            "good": [10]},
        "bagre": {    "peak": range(1, 13),
            "good": []},
        "robalo": {    "peak": [9, 10, 11, 12],
            "good": [8]},
        "mojarra": {    "peak": range(1, 13),
            "good": []},
    }
    
    if month in season_data.get("peak", []):
        return 2  # Peak
    elif month in season_data.get("good", []):
        return 1  # Good
    return 0  # Off season

def recommend_fish(lat, lon, weather, tides, month=None):
    """Genera recomendaciones de peces"""
    if month is None:
        month = get_current_month()
    
    # Obtener temperatura del agua
    water_temp = weather.get("water_temperature") or weather.get("temperature") or 22
    
    # Score de temporada
    season = get_season_score(month, lat)
    
    # Importar base de datos
    from src.fish_db import FISH_SPECIES
    
    # Filtrar peces por ubicación
    candidates = []
    for fish_id, fish in FISH_SPECIES.items():
        # Verificar ubicación (cerca de coordenadas)
        location_match = False
        fish_locs = fish.get("best_locations", [])
        
        # Determinar región
        region = get_region(lat, lon)
        for loc in fish_locs:
            if region.lower() in loc.lower() or loc.lower() in region.lower():
                location_match = True
                break
        
        if not location_match and fish_locs:
            # Verificar sinonimoscommon
            if "cabo" in region.lower() and any("cabo" in l.lower() for l in fish_locs):
                location_match = True
            elif "la paz" in region.lower() and any("la paz" in l.lower() for l in fish_locs):
                location_match = True
        
        if location_match:
            candidates.append((fish_id, fish))
    
    if not candidates:
        # Default a especies comunes
        candidates = [
            ("huachinango", FISH_SPECIES["huachinango"]),
            ("pargo", FISH_SPECIES["pargo"]),
            ("dorado", FISH_SPECIES["dorado"]),
            ("cabrilla", FISH_SPECIES["cabrilla"]),
            ("mojarra", FISH_SPECIES["mojarra"]),
        ]
    
    # Evaluar cada pez
    recommendations = []
    for fish_id, fish in candidates:
        score = 50  # Base score
        
        # Temperatura del agua
        fish_temp_range = fish.get("water_temp", "").replace("°C", "")
        if water_temp:
            temp_ok = evaluate_temp(water_temp, fish_temp_range)
            score += temp_ok * 20
        
        # Temporada
        season_score = get_season_score(month, lat)
        if season_score >= 2:
            score += 20
        elif season_score >= 1:
            score += 10
        
        # Por dificultad
        diff = fish.get("difficulty", "intermedio")
        if diff == "principiante":
            difficulty_bonus = 10
        elif diff == "intermedio":
            difficulty_bonus = 5
        else:
            difficulty_bonus = 0
        score += difficulty_bonus
        
        recommendations.append({
            "fish_id": fish_id,
            "name": fish.get("name"),
            "scientific": fish.get("scientific"),
            "español": fish.get("español"),
            "description": fish.get("description"),
            "size_range": fish.get("size_range"),
            "best_season": fish.get("best_season"),
            "techniques": fish.get("techniques", []),
            "lures": fish.get("lures", []),
            "baits": fish.get("baits", []),
            "difficulty": fish.get("difficulty"),
            "food_value": fish.get("food_value"),
            "score": min(100, max(0, score)),
            "tips": generate_tips(fish_id, weather, tides)
        })
    
    # Ordenar por score
    recommendations.sort(key=lambda x: x["score"], reverse=True)
    
    return recommendations[:6]  # Top 6 recomendaciones

def evaluate_temp(current, fish_range):
    """Evalúa si la temperatura es adecuada"""
    try:
        if "-" in fish_range:
            min_t, max_t = map(int, fish_range.split("-"))
            if min_t <= current <= max_t:
                return 2
            elif abs(current - min_t) <= 3 or abs(current - max_t) <= 3:
                return 1
            return -1
    except:
        pass
    return 0

def generate_tips(fish_id, weather, tides):
    """Genera consejos específicos"""
    tips = []
    
    # Por hora del día
    hour = datetime.now().hour
    if 5 <= hour <= 8:
        tips.append("🎣 Amanecer es el mejor momento - peces activos alimentándose")
    elif 17 <= hour <= 19:
        tips.append("🌅 Atardecer excellent - otra ventana de alimentación")
    elif 10 <= hour <= 16:
        tips.append("☀️ Mediodía - busca agua más profunda o sombra")
    else:
        tips.append("🌙 De noche - usa sonido o cebo vivo")
    
    # Por marea
    if tides.get("is_incoming"):
        tips.append("🌊 MareaSubiendo - peces cerca de costa")
    elif tides.get("is_outgoing"):
        tips.append("🌊 Bajando - peces buscando comida")
    
    # Por temperaturadel agua
    water_temp = weather.get("water_temperature") or weather.get("temperature", 20)
    if water_temp < 18:
        tips.append("🥶 Agua fría - pesca a mayor profundidad")
    elif water_temp > 28:
        tips.append("🔥 Agua caliente - pesca temprano o usa señuelos pequeños")
    
    # Por viento
    wind = weather.get("wind_speed", 0)
    if wind > 25:
        tips.append("💨 Mucho viento - considera pesca desde orilla")
    elif wind < 5:
        tips.append("🌿 Poco viento - ideales señuelos superficie")
    
    # Por específico
    fish_tips = {
        "dorado": ["Usa señuelos coloridos superficiales", "Busca cardúmenes en superficie"],
        "huachinango": ["Pesca de fondo o drifting", "Usa sardina fresca"],
        "pargo": ["Usa cebo fresco en fondo", "Paciencia - muerden suave"],
        "trucha": ["Mosca pequeña al amanecer", "Busca sombras de árboles"],
        "tuna": ["Alta velocidad trolling", "Busca pájaros sobre cardumen"],
    }
    
    specific = fish_tips.get(fish_id, [])
    tips.extend(specific[:2])
    
    return tips

def get_best_times(lat, weather, tides):
    """ Obtiene mejores horarios"""
    times = []
    
    # Amanecer (5-7)
    times.append({
        "time": "05:00 - 07:00",
        "period": "amanecer",
        "reason": "Activos alimentándose después de la noche",
        "rating": 9
    })
    
    # Mañana (7-10)
    times.append({
        "time": "07:00 - 10:00",
        "period": "mañana",
        "reason": "Agua aún fresca",
        "rating": 7
    })
    
    # Mediodía (10-14)
    times.append({
        "time": "10:00 - 14:00",
        "period": "mediodía",
        "reason": "Buscar sombra o agua profunda",
        "rating": 4
    })
    
    # Atardecer (17-19)
    times.append({
        "time": "17:00 - 19:00",
        "period": "atardecer",
        "reason": "Otra ventana de alimentación",
        "rating": 9
    })
    
    # Noche (19-22)
    times.append({
        "time": "19:00 - 22:00",
        "period": "noche",
        "reason": "Peces fundo activos",
        "rating": 6
    })
    
    return times

def get_best_baits(fish_recs):
    """Extrae las carnadas más mencionadas"""
    baits_mentioned = {}
    
    for rec in fish_recs:
        for bait in rec.get("baits", []):
            if bait not in baits_mentioned:
                baits_mentioned[bait] = 0
            baits_mentioned[bait] += rec.get("score", 50) // 20
    
    # Ordenar
    sorted_baits = sorted(baits_mentioned.items(), key=lambda x: x[1], reverse=True)
    return [b[0] for b in sorted_baits[:5]]

def get_region(lat, lon):
    """Determina la región de pesca"""
    # México Pacific
    if 22 <= lat <= 25 and -115 <= lon <= -109:
        return "La Paz / Los Cabos"
    elif 23 <= lat <= 24 and -107 <= lon <= -105:
        return "Mazatlán"
    elif 30 <= lat <= 33 and -117 <= lon <= -115:
        return "Ensenada / Baja California"
    elif 19 <= lat <= 21 and -105 <= lon <= -103:
        return "Manzanillo / Colima"
    elif lat > 25 and lat < 30:
        return "Baja California"
    # USA West Coast
    elif lat > 30 and lon < -115:
        return "California / USA"
    
    return "Costa del Pacífico" 

# Generar guía completa
def generate_fishing_guide(lat, lon, weather, tides, location=None):
    """Genera guía completa de pesca"""
    from src.fish_db import FISH_SPECIES
    
    region_name = location or get_region(lat, lon)
    
    fish_recs = recommend_fish(lat, lon, weather, tides)
    best_times = get_best_times(lat, weather, tides)
    best_baits = get_best_baits(fish_recs)
    
    # Calcular score general
    base_score = 50
    
    temp = weather.get("temperature") or 22
    if 18 <= temp <= 28:
        base_score += 20
    
    wind = weather.get("wind_speed") or 10
    if 5 <= wind <= 20:
        base_score += 15
    
    if tides and tides.get("tides"):
        base_score += 10
    
    fishing_score = min(100, base_score)
    
    # Encontrar alternativas si el score es bajo
    alternatives = []
    alert_message = None
    if fishing_score < 60:
        alternatives = find_alternative_locations(lat, lon, weather, max_distance_km=150)
        if alternatives:
            alert_message = f"Las condiciones en {region_name} no son ideales. Te recomendamos otros sitios cercanos:"
    
    return {
        "location": region_name,
        "location_requested": location,
        "coordinates": {"lat": lat, "lon": lon},
        "fishing_score": fishing_score,
        "conditions": {
            "temperature": temp,
            "water_temp": weather.get("water_temperature") or temp - 2,
            "wind": weather.get("wind_speed"),
            "humidity": weather.get("humidity"),
            "pressure": weather.get("pressure"),
            "condition": weather.get("weather_description"),
        },
        "sun": {
            "sunrise": "06:15",
            "sunset": "19:30"
        },
        "tides": {
            "next_high": tides.get("next_tide", {}).get("time"),
            "next_low": None,
            "coefficient": tides.get("tide_coefficient")
        },
        "recommendations": fish_recs,
        "best_times": best_times,
        "best_baits": best_baits,
        "alternative_locations": alternatives,
        "alert_message": alert_message,
        "tips": [
            f"🔹 Sector: {region_name}",
            f"🔹 Mejor temperatura agua: 20-26°C",
            "🔹 Siempre lleva agua potable",
            "🔹 Protector solar esencial",
            "🔹 Revisa el clima antes de salir"
        ]
    }