import httpx
import os
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, Query # Added Query import just in case
from pydantic import BaseModel
from typing import List, Any
from app.services import astronomy # <-- NEW

# Standard imports needed if not already present in your file structure
from app.services.firebase_auth import get_current_user

router = APIRouter() # Ensure router is defined

NASA_BASE_URL = "https://api.nasa.gov/DONKI"
API_KEY = os.getenv("NASA_API_KEY")

class TechImpact(BaseModel):
    gps_status: str
    radio_status: str
    grid_status: str
    satellite_drag: str

class SpaceWeatherData(BaseModel):
    solar_risk_level: str
    kp_index: float
    tech_impact: TechImpact
    message: str
    astronomy: dict # <-- NEW FIELD

@router.get("/status")
async def get_space_weather(
    user: dict = Depends(get_current_user)
    # We will use the user's saved location logic inside here ideally, 
    # but for simplicity/speed let's default to Nairobi or passed params if we refactor.
    # To keep it simple for now, we'll hardcode the astronomy check to the fixed lat/lon 
    # or rely on the frontend passing it if we changed the endpoint signature.
    # LET'S UPDATE THE ENDPOINT TO ACCEPT LAT/LON
):
    pass # Replaced below

@router.get("/status")
async def get_space_status(
    lat: float = Query(-1.29, description="Lat"), # Default Nairobi
    lon: float = Query(36.82, description="Lon"), 
    user: dict = Depends(get_current_user)
):
    """
    Fetches Space Weather (NASA) + Stargazing Info (Ephem).
    """
    # 1. NASA DATA (Existing Logic)
    kp_index = 1.0
    if API_KEY:
        try:
            async with httpx.AsyncClient() as client:
                end_date = datetime.utcnow().strftime("%Y-%m-%d")
                start_date = (datetime.utcnow() - timedelta(days=3)).strftime("%Y-%m-%d")
                gst_resp = await client.get(f"{NASA_BASE_URL}/GST", params={"startDate": start_date, "endDate": end_date, "api_key": API_KEY})
                if gst_resp.status_code == 200:
                    data = gst_resp.json()
                    for storm in data:
                        for obs in storm.get("allKpIndex", []):
                            k = obs.get("kpIndex", 0)
                            if k > kp_index: kp_index = k
        except Exception: pass

    # Tech Impact Logic
    gps, radio, grid, drag, risk, msg = "Precision", "Clear", "Stable", "Nominal", "Low", "Systems Nominal"
    if kp_index >= 6: 
        risk, msg = "High", "Warning: Solar Storm Active"
        gps = "Degraded"

    # 2. ASTRONOMY DATA (New Logic)
    astro_data = astronomy.get_sky_forecast(lat, lon)

    return SpaceWeatherData(
        solar_risk_level=risk,
        kp_index=kp_index,
        tech_impact=TechImpact(gps_status=gps, radio_status=radio, grid_status=grid, satellite_drag=drag),
        message=msg,
        astronomy=astro_data # <-- Return the star data
    )