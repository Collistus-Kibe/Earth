from fastapi import APIRouter, Depends, HTTPException, Query
from app.services.firebase_auth import get_current_user
from app.services import open_meteo

router = APIRouter()

@router.get("/forecast")
async def get_weather_forecast(
    lat: float = Query(None),
    lon: float = Query(None),
    user: dict = Depends(get_current_user)
):
    target_lat = lat if lat is not None else -1.2921
    target_lon = lon if lon is not None else 36.8219

    try:
        # Strictly fetches real data or cache
        data = await open_meteo.get_7_day_forecast(target_lat, target_lon)
        return data
    except Exception as e:
        print(f"Critical Weather Error: {e}")
        # VIOLATION PREVENTION: Do NOT return fake data. Return 503 Service Unavailable.
        raise HTTPException(status_code=503, detail="Weather Service Unavailable. No connection to Sensor Grid.")