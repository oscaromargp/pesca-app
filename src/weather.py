import requests

def get_weather(lat, lon):
    """Get weather forecast from Open-Meteo (free, no API key)"""
    try:
        # Current weather
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": ["temperature_2m", "relative_humidity_2m", "wind_speed_10m", "wind_direction_10m", 
                       "precipitation", "cloud_cover", "pressure_msl"],
            "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum", "wind_speed_10m_max"],
            "timezone": "auto",
            "forecast_days": 3
        }
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        
        current = data.get("current", {})
        daily = data.get("daily", {})
        
        return {
            "temperature": current.get("temperature_2m"),
            "humidity": current.get("relative_humidity_2m"),
            "wind_speed": current.get("wind_speed_10m"),
            "wind_direction": current.get("wind_direction_10m"),
            "precipitation": current.get("precipitation", 0),
            "cloud_cover": current.get("cloud_cover", 50),
            "pressure": current.get("pressure_msl"),
            "daily_max": daily.get("temperature_2m_max", [None])[0],
            "daily_min": daily.get("temperature_2m_min", [None])[0],
            "forecast": daily
        }
    except Exception as e:
        return {"error": str(e), "temperature": 25, "wind_speed": 10, "cloud_cover": 50}

def get_marine_weather(lat, lon):
    """Get marine weather data"""
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": ["wave_height", "wave_period", "water_temperature"],
            "timezone": "auto"
        }
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        return data.get("current", {})
    except:
        return {}
