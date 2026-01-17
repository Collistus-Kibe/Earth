from fastapi import APIRouter, Depends, Query
from app.services.firebase_auth import get_current_user
from app.services import open_meteo, earth_engine

router = APIRouter()

@router.get("/flood-trend")
async def get_flood_risk_trend(
    lat: float = Query(None),
    lon: float = Query(None),
    user: dict = Depends(get_current_user)
):
    if lat is None: lat, lon = -1.2921, 36.8219

    # 1. Fetch Data
    forecast = await open_meteo.get_7_day_forecast(lat, lon)
    air_quality = await open_meteo.get_air_quality(lat, lon)
    
    # 2. Base Risk Calculation
    rain_forecast = sum(forecast.get("daily", {}).get("precipitation_sum", [])[:3])
    risk_score = min(100, rain_forecast * 2.5)
    
    # 3. AI Narrator Logic (Tone)
    aqi_status = air_quality.get('status', 'Good')
    aqi_val = air_quality.get('aqi', 40)
    
    if risk_score > 40:
        message = f"Critical Alert: Heavy rain forecast ({round(rain_forecast,1)}mm). Soil saturation probable."
    elif aqi_val > 100:
        message = f"Health Warning: Air quality is {aqi_status}. Respiratory stress likely. Limit outdoor exertion."
    elif aqi_val > 50:
        message = f"Air quality is moderate. Conditions are stable, but sensitive groups should mask up."
    else:
        message = "Planetary systems are nominal. Air is crisp and soil is stable. No threats detected."

    # 4. Satellite Adjustment
    vhi = earth_engine.calculate_vhi_score(lat, lon)
    if vhi and vhi['score'] < 30: 
        risk_score += 15
        message += " Note: Satellite detects vegetation stress."

    return {
        "analysis": {
            "next_week_score": max(10, min(98, int(risk_score))),
            "message": message,
            "air_quality": air_quality # Send to frontend
        }
    }