from fastapi import APIRouter, Depends, HTTPException, Query
from app.services.firebase_auth import get_current_user

# Import all our services and models
from app.services import open_meteo
from app.services import google_maps
from app import processing

router = APIRouter()

@router.get("/local-summary")
async def get_local_intelligence_summary(
    lat: float = Query(..., description="User's latitude", ge=-90, le=90),
    lon: float = Query(..., description="User's longitude", ge=-180, le=180),
    user: dict = Depends(get_current_user)
):
    """
    This is the new fusion endpoint for the "Local Intelligence" widget.
    It combines weather, air quality, and fire risk into a single score.
    """
    print(f"User {user.get('email')} requesting local intelligence for ({lat}, {lon})")
    
    try:
        # 1. Get Raw Weather Data
        weather_data = await open_meteo.get_raw_weather_data(lat, lon)
        
        # 2. Get Air Quality Data
        aqi_data = await google_maps.get_air_quality(lat, lon)
        
        # 3. Calculate Fire Risk
        fire_risk = processing.calculate_fwi(
            temp_c=weather_data.temp_max,
            humidity_rh=weather_data.humidity_min,
            wind_kmh=weather_data.wind_max,
            rain_mm=weather_data.precipitation
        )
        
        # 4. Calculate Final Safety Score
        aqi_value = aqi_data.aqi if aqi_data else None
        safety_score_data = processing.calculate_safety_score(fire_risk, aqi_value)
        
        # 5. Return the complete package
        return {
            "safety_score": safety_score_data["score"],
            "primary_risk": safety_score_data["primary_risk"],
            "weather": {
                "temperature": weather_data.temp_max,
                "precipitation": weather_data.precipitation
            },
            "air_quality": {
                "aqi": aqi_value,
                "display_name": aqi_data.display_name if aqi_data else "N/A"
            },
            "fire_risk": round(fire_risk)
        }
        
    except Exception as e:
        print(f"Error in local-summary endpoint: {e}")
        # This will catch errors from get_raw_weather_data if it fails
        raise HTTPException(status_code=500, detail=f"Failed to generate local summary: {e}")