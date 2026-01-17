from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os
import json

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path)

from app.services.firebase_auth import initialize_firebase
from app.services.earth_engine import init_gee 
from app.models.database import Base, engine

# Routers
from app.api.v1 import general as general_router
from app.api.v1 import preferences as prefs_router
from app.api.v1 import alerts as alerts_router
from app.api.v1 import weather as weather_router
from app.api.v1 import ocean as ocean_router
from app.api.v1 import nature as nature_router
from app.api.v1 import space as space_router
from app.api.v1 import predictions as predictions_router
from app.api.v1 import satellite as satellite_router
from app.api.v1 import bio as bio_router
from app.api.v1 import infra as infra_router # <-- NEW: Vital Lines

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up EARTH backend...")
    initialize_firebase()
    print("Attempting Google Earth Engine connection...")
    init_gee() 
    
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"DB Error: {e}")

    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        with open(os.path.join(base_dir, 'data', 'world_rivers.json'), 'r', encoding='utf-8') as f:
            app.state.rivers_data = json.load(f)
    except Exception:
        app.state.rivers_data = None

    yield
    print("Shutting down...")

app = FastAPI(title="EARTH Platform", version="1.4.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8001", "http://127.0.0.1:8001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register All Routers
app.include_router(general_router.router, prefix="/api/v1", tags=["General"])
app.include_router(prefs_router.router, prefix="/api/v1/preferences", tags=["Settings"])
app.include_router(weather_router.router, prefix="/api/v1/weather", tags=["Weather"])
app.include_router(alerts_router.router, prefix="/api/v1/alerts", tags=["Alerts"])
app.include_router(ocean_router.router, prefix="/api/v1/ocean", tags=["Ocean"])
app.include_router(nature_router.router, prefix="/api/v1/nature", tags=["Nature"])
app.include_router(space_router.router, prefix="/api/v1/space", tags=["Space"])
app.include_router(predictions_router.router, prefix="/api/v1/predict", tags=["AI"])
app.include_router(satellite_router.router, prefix="/api/v1/satellite", tags=["Satellite"])
app.include_router(bio_router.router, prefix="/api/v1/bio", tags=["Bio-Shield"])
app.include_router(infra_router.router, prefix="/api/v1/infra", tags=["Infrastructure"]) # <-- NEW

@app.get("/")
async def read_root():
    return {"message": "EARTH Engine Online.", "status": "Operational"}