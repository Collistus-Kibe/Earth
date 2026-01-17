import httpx
import os
from datetime import datetime, timedelta
from fastapi import HTTPException
from pydantic import BaseModel
from typing import List

NASA_BASE_URL = "https://api.nasa.gov/DONKI"
API_KEY = os.getenv("NASA_API_KEY")

class SpaceEvent(BaseModel):
    event_type: str
    severity: str
    timestamp: str
    details: str

class TechImpact(BaseModel):
    gps_status: str       # e.g., "Precision (<1m)" or "Degraded (>50m)"
    radio_status: str     # e.g., "Clear" or "Blackout"
    grid_status: str      # e.g., "Stable" or "Voltage Correction Needed"
    satellite_drag: str   # e.g., "Nominal" or "High"

class SpaceWeatherData(BaseModel):
    solar_risk_level: str
    kp_index: float       # The raw number (0-9)
    tech_impact: TechImpact # <-- NEW: Specific Tech Risks
    active_events: List[SpaceEvent]
    message: str

async def get_space_weather() -> SpaceWeatherData:
    """
    Fetches NASA data and calculates 'Tech Impact' for modern infrastructure.
    """
    # Default safe values if API fails
    kp_index = 1.0 
    events = []
    
    if API_KEY:
        try:
            async with httpx.AsyncClient() as client:
                # Get Geomagnetic Storms (GST)
                end_date = datetime.utcnow().strftime("%Y-%m-%d")
                start_date = (datetime.utcnow() - timedelta(days=3)).strftime("%Y-%m-%d")
                
                gst_resp = await client.get(
                    f"{NASA_BASE_URL}/GST", 
                    params={"startDate": start_date, "endDate": end_date, "api_key": API_KEY}
                )
                
                if gst_resp.status_code == 200:
                    data = gst_resp.json()
                    # Find highest Kp in recent storms
                    for storm in data:
                        for obs in storm.get("allKpIndex", []):
                            k = obs.get("kpIndex", 0)
                            if k > kp_index: 
                                kp_index = k
                                
        except Exception as e:
            print(f"NASA API Error: {e}")

    # --- THE "TECH IMPACT" LOGIC ---
    # Translate Kp Index (0-9) into Infrastructure Risk
    
    gps = "Precision (<3m)"
    radio = "Clear"
    grid = "Stable"
    drag = "Nominal"
    risk = "Low"
    msg = "Planetary shield is holding. Systems nominal."

    if kp_index >= 8: # Extreme Storm (G5)
        risk = "EXTREME"
        gps = "Unavailable / Massive Errors"
        radio = "Full Blackout (Days)"
        grid = "Collapse Risk / Damage"
        drag = "Critical (Orbit Loss)"
        msg = "CRITICAL: Major Geomagnetic Storm. Avoid relying on GPS."
    
    elif kp_index >= 6: # Moderate-Strong (G2-G3)
        risk = "High"
        gps = "Degraded (Error ~50m)"
        radio = "Spotty / Fadeouts"
        grid = "Voltage Alarms"
        drag = "High"
        msg = "Warning: Solar storm active. Drone/GPS navigation may drift."
        
    elif kp_index >= 4: # Unsettled
        risk = "Moderate"
        gps = "Minor Jitter"
        radio = "Minor Interference"
        grid = "Stable"
        drag = "Moderate"
        msg = "Solar activity elevated. Minor tech fluctuations possible."

    return SpaceWeatherData(
        solar_risk_level=risk,
        kp_index=kp_index,
        tech_impact=TechImpact(
            gps_status=gps,
            radio_status=radio,
            grid_status=grid,
            satellite_drag=drag
        ),
        active_events=events,
        message=msg
    )