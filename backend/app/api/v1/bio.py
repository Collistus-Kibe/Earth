from fastapi import APIRouter, Depends, Query
from app.services.firebase_auth import get_current_user
from app.services import open_meteo, bio

# --- THIS LINE WAS MISSING OR OVERWRITTEN ---
router = APIRouter() 

@router.get("/status")
async def get_bio_status(
    lat: float = Query(...),
    lon: float = Query(...),
    user: dict = Depends(get_current_user)
):
    """
    Analyzes environmental factors to predict disease outbreaks.
    """
    # 1. Get Context (Weather & Flood Data)
    weather = await open_meteo.get_raw_weather_data(lat, lon)
    flood = await open_meteo.get_flood_data(lat, lon)
    
    # 2. Run Bio Logic
    # We use 'precipitation_forecast_7d' as a proxy for ground wetness
    risk = await bio.analyze_biological_risk(
        temp=weather.temp_max,
        rain_7day=flood.precipitation_forecast_7d
    )
    return risk