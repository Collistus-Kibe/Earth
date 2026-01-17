import httpx
from fastapi import HTTPException

# EONET API v3 endpoint for events
EONET_API_URL = "https://eonet.gsfc.nasa.gov/api/v3/events"

async def fetch_open_events():
    """
    Fetches the 20 most recent "open" natural events from NASA EONET.
    """
    params = {
        "status": "open",
        "limit": 20,
        "days": 30  # Look at events from the last 30 days
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(EONET_API_URL, params=params)
            
            # Raise an exception for bad status codes (4xx or 5xx)
            response.raise_for_status()
            
            return response.json()
            
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Error fetching data from NASA EONET: {e.response.text}"
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503, # Service Unavailable
                detail=f"Error connecting to NASA EONET: {e}"
            )