import requests
from datetime import datetime, timedelta

def get_tides(lat, lon, days=3):
    """Get tide predictions from NOAA CO-OPS API (free, no key needed)"""
    try:
        # Find nearest station
        stations_url = f"https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations.json"
        resp = requests.get(stations_url, timeout=10)
        stations = resp.json().get("stations", [])
        
        # Find closest station
        closest = min(stations, key=lambda s: abs(float(s.get("lat", 0)) - lat) + abs(float(s.get("lng", 0)) - lon))
        station_id = closest.get("id")
        
        # Get tide predictions
        begin = datetime.now().strftime("%Y%m%d")
        end = (datetime.now() + timedelta(days=days)).strftime("%Y%m%d")
        
        url = f"https://api.tidesandcurrents.noaa.gov/api/prod/datagetter"
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
        prev_height = None
        
        for p in predictions:
            height = float(p.get("v", 0))
            time = p.get("t", "")
            is_high = prev_height is not None and height > prev_height and (len(tides) == 0 or height > tides[-1].get("height", 0))
            
            if len(tides) == 0 or (is_high and tides[-1].get("type") != "high"):
                tides.append({
                    "time": time,
                    "height": height,
                    "type": "high" if is_high else "low"
                })
            prev_height = height
        
        return {
            "station": closest.get("name"),
            "station_id": station_id,
            "tides": tides[:days*2],
            "is_incoming": tides[0].get("type") == "low" if tides else True
        }
    except Exception as e:
        return {"error": str(e), "tides": [], "station": "Unknown"}

def get_currents(lat, lon):
    """Get current predictions from NOAA"""
    try:
        url = f"https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations/{lon},{lat}/current.json"
        resp = requests.get(url, timeout=10)
        return resp.json()
    except:
        return {"currents": []}
