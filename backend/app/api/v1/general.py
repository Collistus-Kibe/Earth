from fastapi import APIRouter, Depends
from typing import Dict
from app.services.firebase_auth import get_current_user

router = APIRouter()

@router.get("/health")
async def get_health():
    """
    Public endpoint to check if the API is running.
    """
    return {"status": "ok", "message": "EARTH Backend is running!"}


@router.get("/protected-data", response_model=Dict[str, str])
async def get_protected_data(
    user: dict = Depends(get_current_user)
):
    """
    A secure endpoint that requires a valid Firebase auth token.
    It returns a welcome message using the user's name from the token.
    """
    user_name = user.get("name", "User")
    user_email = user.get("email", "no-email@example.com")
    
    print(f"Access granted for user: {user_email}")
    
    return {
        "message": f"Hello, {user_name}! Welcome to the secure EARTH API.",
        "your_email": user_email,
        "your_uid": user.get("uid")
    }