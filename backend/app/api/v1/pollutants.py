from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import uuid # To generate unique IDs
from datetime import datetime

# Import DB and auth dependencies
from app.models.database import get_db
from app.services.firebase_auth import get_current_user

# Import our new model
from app.models.pollutant import PollutantSource

router = APIRouter()

# --- Pydantic Models for Data Validation ---

class PollutantSourceCreate(BaseModel):
    """Data model for creating a new source."""
    latitude: float
    longitude: float
    description: str | None = None

class PollutantSourcePublic(BaseModel):
    """Data model for returning a source to the client."""
    id: str
    latitude: float
    longitude: float
    description: str | None
    submitted_by_uid: str
    created_at: datetime

    class Config:
        orm_mode = True # Allows mapping from SQLAlchemy model


@router.get("", response_model=list[PollutantSourcePublic])
async def get_all_pollutant_sources(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user) # Secure this endpoint
):
    """
    Fetches all pollutant sources from the database.
    """
    try:
        sources = db.query(PollutantSource).all()
        return sources
    except Exception as e:
        print(f"Error fetching pollutant sources: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch pollutant sources.")

@router.post("", response_model=PollutantSourcePublic) # <-- THIS LINE IS FIXED
async def create_pollutant_source(
    source_data: PollutantSourceCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user) # Get user info from token
):
    """
    Creates a new pollutant source in the database from a user's click.
    """
    user_uid = user.get("uid")
    if not user_uid:
        raise HTTPException(status_code=401, detail="Could not verify user UID from token.")

    try:
        # Create a new PollutantSource object
        new_source = PollutantSource(
            id=str(uuid.uuid4()), # Generate a new unique ID
            latitude=source_data.latitude,
            longitude=source_data.longitude,
            description=source_data.description,
            submitted_by_uid=user_uid
        )
        
        db.add(new_source)
        db.commit()
        db.refresh(new_source) # Get the created object back from the DB
        
        print(f"New pollutant source added by user {user_uid} at ({new_source.latitude}, {new_source.longitude})")
        return new_source
        
    except Exception as e:
        db.rollback()
        print(f"Error creating pollutant source: {e}")
        raise HTTPException(status_code=500, detail="Failed to save pollutant source.")