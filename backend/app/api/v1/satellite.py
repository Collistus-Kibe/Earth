from fastapi import APIRouter, Depends, Query
from app.services.firebase_auth import get_current_user
from app.services import earth_engine

router = APIRouter()

@router.get("/thermal-scan")
async def get_satellite_thermal(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    user: dict = Depends(get_current_user)
):
    """
    Triggers a live Google Earth Engine scan for Thermal Anomalies.
    """
    print(f"User {user.get('uid')} requesting Satellite Scan at {lat}, {lon}")
    result = await earth_engine.scan_thermal_anomaly(lat, lon)
    return result

@router.get("/visual/vegetation")
async def get_vegetation_visual(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    user: dict = Depends(get_current_user)
):
    """
    Returns a URL to a generated Satellite Map Image (NDVI) of the area.
    """
    result = earth_engine.get_vegetation_map_url(lat, lon)
    if not result or not result.get("url"):
        return {"url": "https://via.placeholder.com/500x300?text=Satellite+Offline", "status": "offline"}
    return result

@router.get("/visual/ocean")
async def get_ocean_visual(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    user: dict = Depends(get_current_user)
):
    """
    Returns a URL to a generated Ocean SST Heatmap.
    """
    result = earth_engine.get_ocean_temp_map_url(lat, lon)
    if not result or not result.get("url"):
        return {"url": "https://via.placeholder.com/500x300?text=Ocean+Data+Unavailable", "status": "offline"}
    return result