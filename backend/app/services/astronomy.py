import ephem
from datetime import datetime

def get_sky_forecast(lat: float, lon: float):
    """
    Calculates visible planets and moon phase for the current location.
    """
    observer = ephem.Observer()
    observer.lat = str(lat)
    observer.lon = str(lon)
    observer.date = datetime.utcnow()

    # Celestial bodies to track
    bodies = {
        'Mars': ephem.Mars(),
        'Venus': ephem.Venus(),
        'Jupiter': ephem.Jupiter(),
        'Saturn': ephem.Saturn(),
        'Moon': ephem.Moon()
    }

    visible_planets = []
    
    for name, body in bodies.items():
        body.compute(observer)
        # Altitude > 0 means it is above the horizon
        # Magnitude < 2 means it is bright enough to see with naked eye
        alt = body.alt * 57.2957795 # Convert radians to degrees
        
        if alt > 0:
            visible_planets.append({
                "name": name,
                "status": "Visible Now",
                "brightness": round(body.mag, 1),
                "position": f"{int(alt)}° above horizon"
            })
        else:
            visible_planets.append({
                "name": name,
                "status": "Below Horizon",
                "brightness": round(body.mag, 1),
                "position": "Set"
            })

    # Calculate Moon Phase (0=New, 0.5=Full)
    moon = ephem.Moon()
    moon.compute(datetime.utcnow())
    phase_val = moon.phase # 0 to 100
    
    phase_name = "Crescent"
    if phase_val > 90: phase_name = "Full Moon"
    elif phase_val > 50: phase_name = "Gibbous"
    elif phase_val < 10: phase_name = "New Moon"

    return {
        "moon_phase": f"{phase_name} ({int(phase_val)}%)",
        "planets": visible_planets
    }