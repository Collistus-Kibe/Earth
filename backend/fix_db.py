import os
from dotenv import load_dotenv

# 1. Load Env Vars
load_dotenv() 

from app.models.database import engine, Base
from app.models.preference import UserPreference
# --- CRITICAL FIX: Import User model so the Foreign Key finds the table ---
from app.models.user import User 

print("--- DATABASE REPAIR TOOL ---")

# Debug Check
key = os.getenv("TIDB_CONNECTION_STRING")
if not key:
    print("❌ CRITICAL ERROR: Could not find TIDB_CONNECTION_STRING in .env")
    exit(1)
else:
    print("✅ Environment variables loaded.")

print("Attempting to update UserPreference schema...")

try:
    # 2. Drop the old table
    print("Dropping old 'user_preferences' table...")
    try:
        UserPreference.__table__.drop(engine)
        print("✅ Old table dropped.")
    except Exception as drop_err:
        print(f"⚠️ Warning (table might not exist): {drop_err}")

    # 3. Re-create tables
    # (Because we imported User, create_all ensures the User table exists too)
    print("Re-creating tables with new schema...")
    Base.metadata.create_all(engine)
    
    print("✅ Table re-created successfully!")
    print("You can now restart your backend.")

except Exception as e:
    print(f"❌ Error: {e}")