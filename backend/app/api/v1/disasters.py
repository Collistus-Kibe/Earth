from fastapi import APIRouter, Depends
from app.services.firebase_auth import get_current_user
from app.services import nasa_eonet

router = APIRouter()

@router.get("/eonet-events")
async def get_eonet_events(
    user: dict = Depends(get_current_user)
):
    """
    Secure endpoint to fetch the latest open natural events from NASA EONET.
    """
    print(f"User {user.get('email')} is requesting EONET data.")
    events = await nasa_eonet.fetch_open_events()
    return events