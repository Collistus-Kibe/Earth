import httpx
from fastapi import HTTPException
from pydantic import BaseModel

# Dedicated Soil API endpoint
SOIL_API_URL = "https://api.open-meteo.com/v1/forecast"

class SoilData(BaseModel):
    """
    Pydantic model for standardized Soil data.
    Values are typically in m³/m³ (volumetric water content).
    """
    moisture_surface: float  # 0-1 cm (Quick to dry/wet)
    moisture_deep: float     # 3-9 cm (Stores water, indicates saturation)
    temperature_surface: float # Soil temp at 0cm
    saturation_status: str   # Interpreted status (e.g., "Dry", "Saturated")

def interpret_saturation(moisture: float) -> str:
    """
    Helper to interpret volumetric soil moisture (m³/m³).
    General rule of thumb: > 0.35-0.4 is often saturation point for many soil types.
    """
    if moisture >= 0.40:
        return "Fully Saturated (High Runoff Risk)"
    elif moisture >= 0.30:
        return "Wet"
    elif moisture >= 0.15:
        return "Moist"
    else:
        return "Dry"

async def get_soil_data(lat: float, lon: float) -> SoilData:
    """
    Fetches dynamic soil moisture and temperature data.
    """
    # We request current soil moisture at two depths and surface temperature
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": ["soil_moisture_0_to_1cm", "soil_moisture_3_to_9cm", "soil_temperature_0cm"],
        "timezone": "auto",
        "forecast_days": 1
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(SOIL_API_URL, params=params)
            data = response.json()

            if data.get("error"):
                raise ValueError(data.get("reason", "Unknown Soil API error"))

            response.raise_for_status()
            
            # Take the current hour (index 0)
            hourly = data.get("hourly", {})
            
            m_surface = hourly.get("soil_moisture_0_to_1cm", [0])[0] or 0.0
            m_deep = hourly.get("soil_moisture_3_to_9cm", [0])[0] or 0.0
            t_surface = hourly.get("soil_temperature_0cm", [0])[0] or 0.0
            
            # Interpret the deep moisture for risk analysis
            status = interpret_saturation(m_deep)

            return SoilData(
                moisture_surface=m_surface,
                moisture_deep=m_deep,
                temperature_surface=t_surface,
                saturation_status=status
            )

        except httpx.HTTPStatusError as e:
            print(f"Soil API HTTP Error: {e.response.text}")
            raise HTTPException(
                status_code=e.response.status_code, 
                detail=f"Soil data provider error: {e.response.text}"
            )
        except (httpx.RequestError, ValueError, KeyError) as e:
            print(f"Soil data processing error: {e}") 
            raise HTTPException(status_code=503, detail="Unable to fetch soil data.")