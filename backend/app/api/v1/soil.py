from fastapi import APIRouter, Depends, HTTPException, Query
from app.services.firebase_auth import get_current_user
from app.services import soil

router = APIRouter()

@router.get("/conditions")
async def get_soil_conditions(
    lat: float = Query(..., description="Latitude", ge=-90, le=90),
    lon: float = Query(..., description="Longitude", ge=-180, le=180),
    user: dict = Depends(get_current_user)
):
    """
    Fetches real-time soil moisture and temperature.
    Includes an automated risk assessment for 'Runoff Potential' (Flash Flood risk).
    """
    try:
        soil_data = await soil.get_soil_data(lat, lon)
        
        # Simple logic: If ground is saturated, any rain will cause runoff.
        runoff_risk = "Low"
        if "Saturated" in soil_data.saturation_status:
            runoff_risk = "CRITICAL"
        elif "Wet" in soil_data.saturation_status:
            runoff_risk = "High"

        return {
            "data": soil_data,
            "analysis": {
                "runoff_potential": runoff_risk,
                "implication": f"Ground is {soil_data.saturation_status.lower()}. Flood risk is {runoff_risk} if rain occurs."
            }
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Critical Error in /soil/conditions: {e}")
        raise HTTPException(status_code=500, detail="Internal server error processing soil data.")