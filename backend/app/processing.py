import math
from typing import List
from .helpers import haversine_distance
from .services.usgs import QuakeData # Import the Pydantic model

def calculate_fwi(temp_c: float, humidity_rh: float, wind_kmh: float, rain_mm: float) -> float:
    """
    Calculates a simplified Fire Weather Index (FWI) score (0-100).
    This is a conceptual model based on FWI inputs, not the full CFFDRS.
    """
    
    # 1. Drought Factor (based on rain)
    # More rain = less drought.
    if rain_mm > 10:
        drought_factor = 0.1 # Very wet
    elif rain_mm > 5:
        drought_factor = 0.5
    elif rain_mm > 1:
        drought_factor = 0.8
    else:
        drought_factor = 1.0 # Very dry

    # 2. Temperature Factor
    # Higher temp = higher risk. Clamp at 0.
    temp_factor = max(0, temp_c - 10) / 10.0 
    
    # 3. Humidity Factor
    # Lower humidity = higher risk.
    humidity_factor = max(0, (70 - humidity_rh)) / 20.0

    # 4. Wind Factor
    # More wind = higher risk.
    wind_factor = 1.0 + (wind_kmh / 20.0)

    # Combine factors
    # This is a conceptual weighted product
    raw_score = (temp_factor * 1.5 + humidity_factor * 1.0) * wind_factor * drought_factor * 20
    
    # Normalize and clamp the score
    final_score = max(0, min(100, raw_score))
    
    return final_score


def calculate_safety_score(
    fire_risk: float, 
    aqi: int | None
) -> dict:
    """
    Calculates a "Personal Earth Safety Score" (0-100)
    and provides a primary risk factor.
    
    Score: 100 = Perfectly Safe, 0 = Extreme Danger
    """
    
    # Start with a perfect score of 100
    total_score = 100.0
    primary_risk = "Low"
    
    # 1. Deduct points for Fire Risk
    # This is the biggest penalty
    if fire_risk > 75:
        total_score -= 70
        primary_risk = "Extreme Fire Risk"
    elif fire_risk > 50:
        total_score -= 40
        primary_risk = "High Fire Risk"
    elif fire_risk > 20:
        total_score -= 15
        primary_risk = "Moderate Fire Risk"

    # 2. Deduct points for Air Quality
    if aqi is not None:
        if aqi > 150:
            total_score -= 25 # Unhealthy
            if total_score > 50: # Only set if fire isn't worse
                primary_risk = "Poor Air Quality"
        elif aqi > 100:
            total_score -= 15 # Unhealthy for sensitive groups
            if total_score > 70:
                primary_risk = "Poor Air Quality"
        elif aqi > 50:
            total_score -= 5 # Moderate
            if total_score > 85:
                primary_risk = "Moderate Air Quality"

    # Clamp the final score
    final_score = max(0, min(100, total_score))
    
    return {
        "score": round(final_score),
        "primary_risk": primary_risk
    }


def calculate_flood_risk(
    user_lat: float,
    user_lon: float,
    precipitation_forecast_7d: float,
    soil_moisture_current: float,
    rivers_data: dict  # This is the loaded world_rivers.json
) -> float:
    """
    Calculates a Flood Probability Score (0-100) by fusing
    rain forecast, soil moisture, and proximity to rivers.
    """
    base_risk = 0.0

    # 1. Rain Factor (Primary Driver)
    if precipitation_forecast_7d > 100: # Over 100mm in 7 days
        base_risk += 40
    elif precipitation_forecast_7d > 50:
        base_risk += 20
    elif precipitation_forecast_7d > 25:
        base_risk += 10
        
    # 2. Soil Moisture Factor (Risk Multiplier)
    # soil_moisture is in m³/m³ (e.g., 0.1 to 0.5)
    soil_multiplier = 1.0
    if soil_moisture_current > 0.4: # Very saturated
        soil_multiplier = 2.0
    elif soil_moisture_current > 0.3:
        soil_multiplier = 1.5
    
    # Apply multiplier
    base_risk = base_risk * soil_multiplier

    # 3. Proximity to River Factor (Risk Adder)
    # This is your Naivasha logic.
    min_dist_to_river = 99999 # Start with a huge distance
    
    if rivers_data:
        for feature in rivers_data.get("features", []):
            try:
                # A river is a LineString (list of points)
                for coords in feature.get("geometry", {}).get("coordinates", []):
                    river_lon, river_lat = coords[0], coords[1] # Take first point
                    dist = haversine_distance(user_lat, user_lon, river_lat, river_lon)
                    if dist < min_dist_to_river:
                        min_dist_to_river = dist
            except Exception:
                continue # Skip malformed river data

    # Add risk based on distance
    if min_dist_to_river < 10: # < 10km from a major river/lake
        base_risk += 30
    elif min_dist_to_river < 25:
        base_risk += 15
    elif min_dist_to_river < 50:
        base_risk += 5

    # 4. Final clamping
    final_score = max(0, min(100, base_risk))
    
    return round(final_score)


def find_closest_quake(
    user_lat: float,
    user_lon: float,
    quake_data: QuakeData
) -> dict | None:
    """
    Finds the closest significant earthquake to the user.
    """
    closest_quake = None
    min_distance = float('inf')

    for quake in quake_data.features:
        distance = haversine_distance(user_lat, user_lon, quake.lat, quake.lon)
        if distance < min_distance:
            min_distance = distance
            closest_quake = quake
            
    if closest_quake:
        return {
            "mag": closest_quake.mag,
            "place": closest_quake.place,
            "time": closest_quake.time,
            "url": closest_quake.url,
            "distance_km": round(min_distance, 2)
        }
    
    return None


def generate_proactive_alerts(
    fire_risk: float,
    flood_risk: float,
    uv_index: float | None
) -> List[str]:
    """
    Checks all risk scores and generates a list of human-readable
    alert messages for the user.
    """
    alerts = []

    # 1. Check Flood Risk (Your Naivasha example)
    if flood_risk > 75:
        alerts.append("CRITICAL: FLOODING MAY OCCUR IN YOUR AREA. EVACUATE LOW-LYING AREAS.")
    elif flood_risk > 50:
        alerts.append("WARNING: High flood probability detected. Monitor local river levels.")
    
    # 2. Check Fire Risk
    if fire_risk > 75:
        alerts.append("CRITICAL: Extreme Fire Risk detected. Be ready to evacuate.")
    elif fire_risk > 50:
        alerts.append("WARNING: High Fire Risk detected. Avoid all outdoor burning.")

    # 3. Check UV Index (Your Nairobi example)
    if uv_index is not None:
        if uv_index >= 11:
            alerts.append("HEALTH: Extreme UV Index (11+) forecast. Avoid sun exposure.")
        elif uv_index >= 8:
            alerts.append("HEALTH: Very High UV Index (8-10) forecast. Stay indoors or seek shade.")

    # 4. If no risks, return a safe message
    if not alerts:
        alerts.append("All Clear: No immediate environmental threats detected for your area.")
        
    return alerts