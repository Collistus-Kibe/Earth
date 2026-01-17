import httpx
from pydantic import BaseModel

AIR_API_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"

class AirData(BaseModel):
    aqi: float
    co: float    # Carbon Monoxide (Traffic/Burning)
    no2: float   # Nitrogen Dioxide (Industry/Cars)
    pm25: float  # Dust/Smoke
    status: str  # "Clean", "Polluted", "Toxic"

async def get_pollution_levels(lat: float, lon: float) -> AirData:
    """
    Fetches indicators of 'Bad Human Activity' (CO, NO2).
    """
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": ["european_aqi", "carbon_monoxide", "nitrogen_dioxide", "pm2_5"],
        "timezone": "auto"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(AIR_API_URL, params=params)
            data = response.json()
            
            current = data.get("current", {})
            aqi = current.get("european_aqi", 0)
            co = current.get("carbon_monoxide", 0)
            
            # Determine Status based on CO (Carbon Monoxide)
            # CO > 300 µg/m³ usually implies heavy traffic/burning
            status = "Clean"
            if aqi > 80: status = "Toxic"
            elif aqi > 50: status = "Polluted"
            elif co > 350: status = "High Emissions"
            
            return AirData(
                aqi=aqi,
                co=co,
                no2=current.get("nitrogen_dioxide", 0),
                pm25=current.get("pm2_5", 0),
                status=status
            )
        except Exception as e:
            print(f"Air Quality Error: {e}")
            return AirData(aqi=0, co=0, no2=0, pm25=0, status="Unknown")