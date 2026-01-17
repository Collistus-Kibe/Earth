from fastapi import APIRouter, Depends, HTTPException, Query
from app.services.firebase_auth import get_current_user
from app.services import biodiversity

router = APIRouter()

@router.get("/check-sensitivity")
async def check_ecological_sensitivity(
    lat: float = Query(..., description="Latitude", ge=-90, le=90),
    lon: float = Query(..., description="Longitude", ge=-180, le=180),
    user: dict = Depends(get_current_user)
):
    """
    Analyzes the location for ecological sensitivity.
    Returns a list of Critically Endangered species found within ~5km.
    """
    try:
        eco_data = await biodiversity.check_biodiversity_risk(lat, lon)
        return eco_data
    except Exception as e:
        print(f"Error in /nature/check-sensitivity: {e}")
        raise HTTPException(status_code=500, detail="Internal server error processing biodiversity data.")