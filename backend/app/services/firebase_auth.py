import firebase_admin
from firebase_admin import credentials, auth
from fastapi import Request, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import os

# --- Import DB and User Model ---
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.user import User
# -------------------------------

BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FILE_NAME_FROM_ENV = os.getenv("FIREBASE_CREDENTIALS_PATH", "firebase-service-account.json")
SERVICE_ACCOUNT_FILE = os.path.join(BACKEND_DIR, FILE_NAME_FROM_ENV)

def initialize_firebase():
    """
    Initializes the Firebase Admin SDK.
    """
    try:
        firebase_admin.get_app()
    except ValueError:
        print(f"Initializing Firebase with cert: {SERVICE_ACCOUNT_FILE}")
        cred = credentials.Certificate(SERVICE_ACCOUNT_FILE)
        firebase_admin.initialize_app(cred)
    print("Firebase Admin SDK initialized.")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)  # <-- ADDED DATABASE DEPENDENCY
):
    """
    Dependency to:
    1. Verify Firebase ID token.
    2. Get or Create the user in the TiDB database.
    3. Return the user's token data.
    """
    try:
        decoded_token = auth.verify_id_token(token)
    except auth.ExpiredIdTokenError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except auth.InvalidIdTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token verification failed: {e}")

    # --- ADDED: TiDB User Sync Logic ---
    uid = decoded_token.get("uid")
    if not uid:
        raise HTTPException(status_code=401, detail="Invalid token: No UID found")

    try:
        # Check if user exists in our DB
        db_user = db.query(User).filter(User.uid == uid).first()

        if not db_user:
            # User is new, create them in our TiDB
            print(f"New user detected. Creating user {uid} in TiDB.")
            new_user = User(
                uid=uid,
                email=decoded_token.get("email"),
                display_name=decoded_token.get("name")
            )
            db.add(new_user)
            db.commit()
        else:
            # Optional: Update user info if it has changed
            if db_user.display_name != decoded_token.get("name") or db_user.email != decoded_token.get("email"):
                db_user.display_name = decoded_token.get("name")
                db_user.email = decoded_token.get("email")
                db.commit()
                
    except Exception as e:
        # Don't fail the request if DB fails, but log it
        print(f"CRITICAL: Failed to sync user {uid} to TiDB. Error: {e}")
        # In a production app, you might want to handle this more gracefully
        # For now, we'll just log and continue.
    
    # --- END: TiDB User Sync Logic ---

    return decoded_token