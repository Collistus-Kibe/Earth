import httpx
from fastapi import HTTPException
from pydantic import BaseModel
from typing import List

# We use the dedicated Marine API endpoint from Open-Meteo
# This sources data from Copernicus Global Sea (CMEMS) and others.
MARINE_API_URL = "https://marine-api.open-meteo.com/v1/marine"

class MarineData(BaseModel):
    """
    Pydantic model for standardized Marine data.
    """
    wave_height_max: float      # Max significant wave height (meters)
    wave_direction_dominant: int # Dominant wave direction (degrees)
    sea_surface_temp: float     # Mean Sea Surface Temperature (°C)
    current_velocity: float     # Ocean current speed (km/h) -- critical for drift predictions

async def get_marine_data(lat: float, lon: float) -> MarineData:
    """
    Fetches critical ocean physics data for the given location.
    """
    # We request daily aggregations to get the "big picture" risks
    # We request current_weather to get real-time SST
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": ["wave_height_max", "wave_direction_dominant"],
        "hourly": ["ocean_current_velocity", "sea_surface_temperature"],
        "timezone": "auto",
        "forecast_days": 1
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(MARINE_API_URL, params=params)
            data = response.json()

            if data.get("error"):
                # This happens if you request marine data for a land location (e.g. Nairobi)
                # We handle this gracefully so the app doesn't crash.
                if data.get("reason") == "Location is on land":
                    return None 
                raise ValueError(data.get("reason", "Unknown Marine API error"))

            response.raise_for_status()
            
            # --- Parse Daily Data (Waves) ---
            daily = data.get("daily", {})
            wave_height = daily.get("wave_height_max", [0.0])[0]
            wave_dir = daily.get("wave_direction_dominant", [0])[0]
            
            # --- Parse Hourly Data (SST & Currents) ---
            # We just take the current hour (index 0) for "now"
            hourly = data.get("hourly", {})
            sst_list = hourly.get("sea_surface_temperature", [])
            current_list = hourly.get("ocean_current_velocity", [])
            
            # Default to 0.0 if data is missing (safety check)
            sst = sst_list[0] if sst_list else 0.0
            current_vel = current_list[0] if current_list else 0.0

            return MarineData(
                wave_height_max=wave_height,
                wave_direction_dominant=wave_dir,
                sea_surface_temp=sst,
                current_velocity=current_vel
            )

        except httpx.HTTPStatusError as e:
            print(f"Marine API HTTP Error: {e.response.text}")
            raise HTTPException(
                status_code=e.response.status_code, 
                detail=f"Marine data provider error: {e.response.text}"
            )
        except (httpx.RequestError, ValueError, KeyError) as e:
            print(f"Marine data processing error: {e}") 
            # We return None here so the UI shows "Not Applicable" instead of crashing
            return None