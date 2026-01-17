from fastapi import APIRouter, Depends, HTTPException, Query, Request # <-- ADD Request
from sqlalchemy.orm import Session # <-- ADD Session
from app.services.firebase_auth import get_current_user

# --- UPDATED IMPORTS ---
from app.services import open_meteo
from app import processing
from app.models.database import get_db # <-- ADD get_db
from app.models.preference import UserPreference # <-- ADD UserPreference
# -----------------------

router = APIRouter()

@router.get("/fire-weather")
async def get_fire_weather_risk(
    lat: float = Query(..., description="User's latitude", ge=-90, le=90),
    lon: float = Query(..., description="User's longitude", ge=-180, le=180),
    user: dict = Depends(get_current_user)
):
    """
    Calculates the Fire Weather Index (FWI) risk for a specific location
    by fetching raw data and running it through the processing model.
    """
    print(f"User {user.get('email')} requesting fire risk for ({lat}, {lon})")
    
    try:
        # 1. Fetch the raw weather data
        weather_data = await open_meteo.get_raw_weather_data(lat, lon)
        
        # 2. Run data through our local processing model
        fwi_score = processing.calculate_fwi(
            temp_c=weather_data.temp_max,
            humidity_rh=weather_data.humidity_min,
            wind_kmh=weather_data.wind_max,
            rain_mm=weather_data.precipitation
        )
        
        # 3. Return the calculated score
        return {
            "fwi_score": fwi_score,
            "location": {
                "latitude": lat,
                "longitude": lon
            },
            "raw_data": weather_data.dict() # Send raw data for debugging
        }
        
    except HTTPException as e:
        # Re-raise HTTPExceptions from services
        raise e
    except Exception as e:
        print(f"Error in fire-weather endpoint: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate fire risk insight.")

# --- NEW FLOOD RISK ENDPOINT ---

@router.get("/flood")
async def get_flood_risk(
    request: Request, # To access app.state
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    Calculates the Flood Probability risk for the user's
    saved home location.
    """
    user_uid = user.get("uid")

    # 1. Get user's home location from TiDB
    prefs = db.query(UserPreference).filter(UserPreference.user_uid == user_uid).first()
    if not prefs or not prefs.home_latitude:
        raise HTTPException(status_code=404, detail="Home location not set. Please set your location first.")
        
    user_lat = prefs.home_latitude
    user_lon = prefs.home_longitude

    print(f"User {user.get('email')} requesting flood risk for ({user_lat}, {user_lon})")

    try:
        # 2. Get flood-related weather data
        flood_data = await open_meteo.get_flood_data(user_lat, user_lon)
        
        # 3. Get river data from app state
        rivers_data = request.app.state.rivers_data
        if not rivers_data:
            raise HTTPException(status_code=500, detail="River data not loaded on server.")
        
        # 4. Run data through our processing model
        flood_score = processing.calculate_flood_risk(
            user_lat=user_lat,
            user_lon=user_lon,
            precipitation_forecast_7d=flood_data.precipitation_forecast_7d,
            soil_moisture_current=flood_data.soil_moisture_current,
            rivers_data=rivers_data
        )

        # 5. Return the score
        return {
            "flood_score": flood_score,
            "location": { "latitude": user_lat, "longitude": user_lon },
            "debug_data": flood_data.dict()
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error in flood-risk endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate flood risk: {e}")