import httpx
from fastapi import HTTPException
from pydantic import BaseModel
from typing import List, Optional

# USGS API endpoint for significant earthquakes in the past 24 hours
USGS_API_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/significant_hour.geojson"
# Let's use 2.5+ magnitude for the past day for more data
USGS_API_URL_ALL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.geojson"


class QuakeFeature(BaseModel):
    """A Pydantic model for a single earthquake feature."""
    mag: float
    place: str
    time: int
    url: str
    lat: float
    lon: float

class QuakeData(BaseModel):
    """A Pydantic model for the full API response."""
    features: List[QuakeFeature]

async def get_significant_earthquakes() -> QuakeData:
    """
    Fetches all earthquakes with a magnitude of 2.5+ in the last 24 hours.
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(USGS_API_URL_ALL)
            response.raise_for_status() # Raise for 4xx/5xx errors
            
            data = response.json()
            
            # Parse the features
            features_list = []
            for item in data.get("features", []):
                properties = item.get("properties", {})
                geometry = item.get("geometry", {}).get("coordinates", [])
                
                if not properties or len(geometry) < 2:
                    continue

                features_list.append(
                    QuakeFeature(
                        mag=properties.get("mag", 0.0),
                        place=properties.get("place", "Unknown location"),
                        time=properties.get("time", 0),
                        url=properties.get("url", ""),
                        lon=geometry[0], # Lon is first in GeoJSON
                        lat=geometry[1]
                    )
                )
            
            return QuakeData(features=features_list)

        except httpx.HTTPStatusError as e:
            print(f"USGS HTTP Error: {e.response.text}")
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Error fetching data from USGS: {e.response.text}"
            )
        except (httpx.RequestError, ValueError, KeyError) as e:
            print(f"USGS processing error: {e}") 
            raise HTTPException(
                status_code=503,
                detail=f"Earthquake data processing error: {e}"
            )