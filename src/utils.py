import requests

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
            "ip": data.get("ip")
        }
    except:
        return {"lat": 25.7617, "lon": -80.1918, "city": "Miami", "country": "USA"}

def calculate_fishing_score(tide_data, weather_data, solunar_data):
    """Calculate fishing score 1-10 based on multiple factors"""
    score = 5.0
    
    # Tide factor (0-3 points)
    if tide_data.get("is_incoming"):
        score += 1.5
    if tide_data.get("height", 0) > 0.5:
        score += 1.0
    
    # Weather factor (0-3 points)
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
    
    # Solunar factor (0-4 points)
    solunar_rating = solunar_data.get("solunar_rating", 3)
    score += (solunar_rating - 3) * 0.8
    
    # Moon phase bonus
    moon_illumination = solunar_data.get("moon_illumination", 50)
    if 40 < moon_illumination < 60:
        score += 0.5
    
    return max(1, min(10, round(score, 1)))
