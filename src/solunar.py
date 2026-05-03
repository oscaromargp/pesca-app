from skyfield.api import load, Topos
from datetime import datetime, timedelta
import math

def get_solunar_data(lat, lon, date=None):
    """Calculate solunar data using Skyfield (local, no API needed)"""
    try:
        if date is None:
            date = datetime.now()
        
        # Load ephemeris data
        eph = load('de421.bsp')
        ts = load.timescale()
        earth = eph['earth']
        moon = eph['moon']
        sun = eph['sun']
        
        # Location
        location = earth + Topos(latitude_degrees=lat, longitude_degrees=lon)
        
        # Current time
        t = ts.from_datetime(date)
        
        # Moon position
        astrom = (moon - location).at(t)
        alt, az, distance = astrom.apparent().altaz()
        
        # Moon phase (0=new, 100=full)
        sun_astrom = (sun - earth).at(t)
        moon_astrom = (moon - earth).at(t)
        
        elongation = moon_astrom.separation_from(sun_astrom)
        moon_phase = (1 - math.cos(elongation.radians)) * 50
        moon_illumination = round(moon_phase, 1)
        
        # Major periods (moon transit and opposition)
        # Simplified calculation
        major_periods = []
        for hours_offset in [-6, 0, 6]:
            period_time = date + timedelta(hours=hours_offset)
            major_periods.append(period_time.strftime("%H:%M"))
        
        # Minor periods (moonrise and moonset)
        minor_periods = []
        for hours_offset in [-3, 3, 9]:
            period_time = date + timedelta(hours=hours_offset)
            minor_periods.append(period_time.strftime("%H:%M"))
        
        # Solunar rating (1-5) based on moon phase and position
        if 40 < moon_illumination < 60:
            solunar_rating = 5
        elif 30 < moon_illumination < 70:
            solunar_rating = 4
        elif 20 < moon_illumination < 80:
            solunar_rating = 3
        elif moon_illumination < 10 or moon_illumination > 90:
            solunar_rating = 2
        else:
            solunar_rating = 1
        
        return {
            "moon_phase": round(moon_phase / 100, 2),
            "moon_illumination": moon_illumination,
            "moon_altitude": round(alt.degrees, 1),
            "major_periods": major_periods[:2],
            "minor_periods": minor_periods[:2],
            "solunar_rating": solunar_rating,
            "best_fishing": solunar_rating >= 4
        }
    except Exception as e:
        # Fallback without Skyfield
        return {
            "moon_phase": 0.5,
            "moon_illumination": 50,
            "moon_altitude": 45,
            "major_periods": ["06:00", "18:00"],
            "minor_periods": ["03:00", "15:00"],
            "solunar_rating": 3,
            "best_fishing": False,
            "error": str(e)
        }
