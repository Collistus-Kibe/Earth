import httpx
from fastapi import HTTPException
import os
from pydantic import BaseModel

# Get the Google Maps API Key you added to your .env file
API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
AIR_QUALITY_URL = "https://airquality.googleapis.com/v1/currentConditions:lookup"

if not API_KEY:
    print("WARNING: GOOGLE_MAPS_API_KEY is not set. Air Quality API will fail.")

class AirQualityData(BaseModel):
    """Holds the parsed Air Quality Index (AQI)"""
    aqi: int
    display_name: str

async def get_air_quality(lat: float, lon: float) -> AirQualityData | None:
    """
    Fetches the current Air Quality Index (AQI) from the Google Air Quality API.
    """
    if not API_KEY:
        # Don't fail the whole request, just return None
        print("Cannot fetch AQI: GOOGLE_MAPS_API_KEY is missing.")
        return None

    client = httpx.AsyncClient()
    try:
        payload = {
            "location": {
                "latitude": lat,
                "longitude": lon
            },
            "extraComputations": ["LOCAL_AQI"],
            "languageCode": "en"
        }
        
        headers = {
            'Content-Type': 'application/json'
        }

        response = await client.post(f"{AIR_QUALITY_URL}?key={API_KEY}", json=payload, headers=headers)
        
        response.raise_for_status() # Raise for 4xx/5xx errors
        
        data = response.json()

        # Parse the response to find the local AQI
        # We look for the "uaqi" (Universal AQI)
        for index in data.get("indexes", []):
            if index.get("code") == "uaqi":
                return AirQualityData(
                    aqi=index.get("aqi"),
                    display_name=index.get("displayName")
                )
        
        # If no uaqi is found, return None
        return None

    except httpx.HTTPStatusError as e:
        print(f"Google Air Quality HTTP Error: {e.response.text}")
        # Don't fail the whole request, just log and return None
        return None
    except Exception as e:
        print(f"Error processing Google Air Quality data: {e}")
        return None
    finally:
        await client.aclose()