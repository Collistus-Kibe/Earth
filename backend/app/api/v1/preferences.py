from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from app.models.database import get_db
from app.services.firebase_auth import get_current_user
from app.models.preference import UserPreference

router = APIRouter()

# --- Models ---
class LocationUpdate(BaseModel):
    latitude: float
    longitude: float
    zoom: int = 10

class SettingsUpdate(BaseModel):
    fcm_token: Optional[str] = None
    sub_weekly_digest: Optional[bool] = None
    sub_astronomy: Optional[bool] = None

# --- Endpoints ---

@router.get("/me")
async def get_my_preferences(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """Get current user settings."""
    user_uid = user.get("uid")
    prefs = db.query(UserPreference).filter(UserPreference.user_uid == user_uid).first()
    if not prefs:
        return {"message": "No preferences set."}
    return prefs

@router.post("/me")
async def update_location(
    loc_data: LocationUpdate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    [RESTORED] This is the endpoint your Dashboard calls to save Location.
    """
    user_uid = user.get("uid")
    print(f"Saving location for {user_uid}: {loc_data.latitude}, {loc_data.longitude}")
    
    prefs = db.query(UserPreference).filter(UserPreference.user_uid == user_uid).first()
    if not prefs:
        prefs = UserPreference(user_uid=user_uid)
        db.add(prefs)
    
    prefs.home_latitude = loc_data.latitude
    prefs.home_longitude = loc_data.longitude
    prefs.default_zoom = loc_data.zoom
    
    try:
        db.commit()
        return {"status": "success", "message": "Location saved."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/settings")
async def update_messaging_settings(
    settings: SettingsUpdate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """Update notifications and tokens."""
    user_uid = user.get("uid")
    prefs = db.query(UserPreference).filter(UserPreference.user_uid == user_uid).first()
    if not prefs:
        prefs = UserPreference(user_uid=user_uid)
        db.add(prefs)

    if settings.fcm_token is not None: prefs.fcm_device_token = settings.fcm_token
    if settings.sub_weekly_digest is not None: prefs.sub_weekly_digest = settings.sub_weekly_digest
    if settings.sub_astronomy is not None: prefs.sub_astronomy_alerts = settings.sub_astronomy

    try:
        db.commit()
        return {"status": "success"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))