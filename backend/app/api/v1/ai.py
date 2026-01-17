from fastapi import APIRouter, Depends, Query
from app.services.firebase_auth import get_current_user
from app.services import narrator

router = APIRouter()

@router.get("/briefing")
async def get_ai_briefing(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    user: dict = Depends(get_current_user)
):
    """
    Returns a Gemini-generated 'Companion' summary of all risks.
    """
    user_name = user.get("name", "Traveler").split(" ")[0] # First name only
    print(f"Generating briefing for {user_name}...")
    
    briefing = await narrator.generate_daily_briefing(lat, lon, user_name)
    
    return {
        "text": briefing,
        "timestamp": "Just now"
    }