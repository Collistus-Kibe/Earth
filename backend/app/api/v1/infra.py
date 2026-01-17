from fastapi import APIRouter, Depends, Query
from app.services.firebase_auth import get_current_user
from app.services import open_meteo

router = APIRouter()

@router.get("/status")
async def get_infrastructure_status(
    lat: float = Query(None),
    lon: float = Query(None),
    user: dict = Depends(get_current_user)
):
    if lat is None: lat, lon = -1.2921, 36.8219

    # 1. Fetch Real Data
    weather = await open_meteo.get_raw_weather_data(lat, lon)
    flood = await open_meteo.get_flood_data(lat, lon)

    # 2. Risk Math (Null-Safe)
    
    # Power: Risks from High Wind (>50km/h) or High Heat (>35C)
    power_risk = "STABLE"
    # Safe checks: Use 0 if values are missing (None)
    wind = weather.wind_max if weather.wind_max is not None else 0
    temp = weather.temp_max if weather.temp_max is not None else 0
    
    if wind > 50: power_risk = "GRID STRESS (WIND)"
    if temp > 35: power_risk = "GRID STRESS (HEAT)"

    # Roads: Risks from Rain (>20mm) or Soil Saturation
    road_risk = "CLEAR"
    rain = flood.precipitation_forecast_7d if flood.precipitation_forecast_7d is not None else 0
    soil = flood.soil_moisture_current if flood.soil_moisture_current is not None else 0
    
    if rain > 20: road_risk = "SLIPPERY"
    if rain > 50: road_risk = "FLOOD RISK"
    # This was the crashing line - now safe
    if soil > 0.4: road_risk = "MUD HAZARD"

    # Net: Risks from extreme conditions
    net_risk = "OPTIMAL"
    if wind > 70: net_risk = "DEGRADED"

    return {
        "power_grid_risk": power_risk,
        "road_network_risk": road_risk,
        "internet_risk": net_risk
    }