from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.services.firebase_auth import get_current_user
from app.models.database import get_db
from app.services import marine

router = APIRouter()

@router.get("/status")
async def get_marine_status(
    lat: float = Query(..., description="Latitude", ge=-90, le=90),
    lon: float = Query(..., description="Longitude", ge=-180, le=180),
    user: dict = Depends(get_current_user)
):
    """
    Fetches real-time ocean physics data (SST, Waves, Currents).
    Returns 404 or a clean "Land Location" message if coordinates are not over water.
    """
    print(f"User {user.get('email')} requesting marine status for ({lat}, {lon})")

    try:
        marine_data = await marine.get_marine_data(lat, lon)
        
        if marine_data is None:
            return {
                "status": "inactive",
                "message": "Location is on land. Marine models are not applicable.",
                "data": None
            }
            
        return {
            "status": "active",
            "message": "Marine data retrieved successfully.",
            "data": marine_data
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Critical Error in /ocean/status: {e}")
        raise HTTPException(status_code=500, detail="Internal server error processing marine data.")