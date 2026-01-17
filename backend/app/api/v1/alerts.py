from fastapi import APIRouter, Depends, HTTPException, Request # <-- ADD Request
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.services.firebase_auth import get_current_user
from app.models.preference import UserPreference
from app.services import nasa_eonet
from app.helpers import haversine_distance

from app.services import usgs
from app import processing

# --- NEW IMPORT ---
from app.services import open_meteo
# -------------------

router = APIRouter()

@router.get("/nearby-events")
async def get_nearby_events(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
    radius_km: int = 500
):
    # ... (existing function, no changes) ...
    user_uid = user.get("uid")
    prefs = db.query(UserPreference).filter(UserPreference.user_uid == user_uid).first()
    if not prefs or not prefs.home_latitude:
        raise HTTPException(status_code=404, detail="Home location not set. Please set your location first.")
    user_lat = prefs.home_latitude
    user_lon = prefs.home_longitude
    try:
        all_events_data = await nasa_eonet.fetch_open_events()
        all_events = all_events_data.get("events", [])
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Failed to fetch NASA EONET data: {e}")
    nearby_events = []
    for event in all_events:
        try:
            geom = event.get("geometry", [])[0]
            if geom.get("type") == "Point":
                event_lon, event_lat = geom.get("coordinates")
            else:
                event_lon, event_lat = geom.get("coordinates")[0][0]
            distance = haversine_distance(user_lat, user_lon, event_lat, event_lon)
            if distance <= radius_km:
                event['distance_km'] = round(distance, 2)
                nearby_events.append(event)
        except Exception as e:
            print(f"Skipping event {event.get('id')}: could not parse coordinates. Error: {e}")
    return {
        "user_location": {"latitude": user_lat, "longitude": user_lon},
        "search_radius_km": radius_km,
        "event_count": len(nearby_events),
        "events": nearby_events
    }

@router.get("/nearby-earthquake")
async def get_nearby_earthquake(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    # ... (existing function, no changes) ...
    user_uid = user.get("uid")
    prefs = db.query(UserPreference).filter(UserPreference.user_uid == user_uid).first()
    if not prefs or not prefs.home_latitude:
        raise HTTPException(status_code=404, detail="Home location not set.")
    user_lat = prefs.home_latitude
    user_lon = prefs.home_longitude
    try:
        quake_data = await usgs.get_significant_earthquakes()
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Failed to fetch USGS data: {e}")
    closest_quake = processing.find_closest_quake(user_lat, user_lon, quake_data)
    if not closest_quake:
        return { "message": "No significant earthquakes found in the last 24 hours." }
    return closest_quake

# --- NEW "PROACTIVE ALERT" ENDPOINT ---

@router.get("/run-check")
async def run_proactive_alert_check(
    request: Request, # To access app.state
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    Simulates the "daily check" by running all models for the user.
    Returns a list of human-readable alert strings.
    """
    user_uid = user.get("uid")

    # 1. Get user's home location
    prefs = db.query(UserPreference).filter(UserPreference.user_uid == user_uid).first()
    if not prefs or not prefs.home_latitude:
        raise HTTPException(status_code=404, detail="Home location not set.")
    user_lat = prefs.home_latitude
    user_lon = prefs.home_longitude
    
    print(f"Running proactive alert check for user {user.get('email')}...")

    try:
        # 2. Fetch all raw data in parallel
        flood_model_data = await open_meteo.get_flood_data(user_lat, user_lon)
        fire_model_data = await open_meteo.get_raw_weather_data(user_lat, user_lon)
        rivers_data = request.app.state.rivers_data
        
        # 3. Run all processing models
        flood_risk = processing.calculate_flood_risk(
            user_lat=user_lat,
            user_lon=user_lon,
            precipitation_forecast_7d=flood_model_data.precipitation_forecast_7d,
            soil_moisture_current=flood_model_data.soil_moisture_current,
            rivers_data=rivers_data
        )
        
        fire_risk = processing.calculate_fwi(
            temp_c=fire_model_data.temp_max,
            humidity_rh=fire_model_data.humidity_min,
            wind_kmh=fire_model_data.wind_max,
            rain_mm=fire_model_data.precipitation
        )
        
        uv_index = flood_model_data.uv_index_tomorrow

        # 4. Generate alert messages
        alerts = processing.generate_proactive_alerts(
            fire_risk=fire_risk,
            flood_risk=flood_risk,
            uv_index=uv_index
        )
        
        return {"alerts": alerts}

    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error in alert-check endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate alerts: {e}")