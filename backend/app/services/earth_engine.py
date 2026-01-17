import ee
import os
import json
from google.oauth2 import service_account
from datetime import datetime, timedelta

# Path to your JSON Key
KEY_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'earth-engine-key.json')

_gee_initialized = False

def init_gee():
    global _gee_initialized
    if _gee_initialized: return True
    try:
        if not os.path.exists(KEY_FILE): return False
        credentials = service_account.Credentials.from_service_account_file(KEY_FILE)
        scoped_credentials = credentials.with_scopes(['https://www.googleapis.com/auth/earthengine'])
        ee.Initialize(credentials=scoped_credentials)
        _gee_initialized = True
        return True
    except Exception as e:
        print(f"GEE Init Error: {e}")
        return False

def calculate_vhi_score(lat: float, lon: float):
    """
    MATHEMATICAL FUSION:
    Combines Vegetation Index (NDVI) and Temperature (LST) to calculate Drought Risk.
    Formula: VHI = (0.5 * VCI) + (0.5 * TCI)
    """
    if not init_gee(): return None

    try:
        point = ee.Geometry.Point([lon, lat])
        region = point.buffer(5000).bounds() # 5km analysis radius

        # 1. Get Vegetation (Sentinel-2)
        s2 = ee.ImageCollection('COPERNICUS/S2_SR') \
            .filterBounds(region) \
            .filterDate((datetime.now() - timedelta(days=14)).strftime('%Y-%m-%d'), datetime.now().strftime('%Y-%m-%d')) \
            .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
            .median()
        
        ndvi = s2.normalizedDifference(['B8', 'B4']) # Math: (NIR-Red)/(NIR+Red)
        mean_ndvi = ndvi.reduceRegion(reducer=ee.Reducer.mean(), geometry=region, scale=100).get('nd').getInfo()

        # 2. Get Temperature (MODIS)
        modis = ee.ImageCollection('MODIS/006/MOD11A1') \
            .filterBounds(region) \
            .filterDate((datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'), datetime.now().strftime('%Y-%m-%d')) \
            .select('LST_Day_1km') \
            .mean()
        
        temp_kelvin = modis.reduceRegion(reducer=ee.Reducer.mean(), geometry=region, scale=1000).get('LST_Day_1km').getInfo()
        
        # Handle Missing Data (Clouds)
        if mean_ndvi is None: mean_ndvi = 0.5
        if temp_kelvin is None: temp_kelvin = 300 # Default to ~27C if blocked

        # 3. The Math (VHI Calculation)
        # Normalize Temp (Assuming 20C-40C range for stress)
        temp_c = (temp_kelvin * 0.02) - 273.15
        thermal_stress_inv = 1.0 - ((temp_c - 20) / 20) # 1.0 is Cool, 0.0 is Hot
        thermal_stress_inv = max(0, min(1, thermal_stress_inv))

        # VHI = 0.5 * Vegetation + 0.5 * ThermalComfort
        vhi = (0.6 * mean_ndvi) + (0.4 * thermal_stress_inv)
        
        # Scale to 0-100 (100 is Best Health)
        final_score = round(vhi * 100, 1)

        return {
            "score": final_score,
            "details": f"Vegetation: {round(mean_ndvi, 2)}, Ground Temp: {round(temp_c, 1)}°C",
            "interpretation": "Healthy" if final_score > 60 else "Stressed (Drought Risk)"
        }

    except Exception as e:
        print(f"GEE Math Error: {e}")
        return None

# [Keep existing visual functions: get_vegetation_map_url, get_ocean_temp_map_url, scan_thermal_anomaly]
# ... (Assume previous visual functions are here or re-paste if needed)
def get_vegetation_map_url(lat, lon):
    # ... (Keep existing code)
    pass 
def get_ocean_temp_map_url(lat, lon):
    # ... (Keep existing code)
    pass
def scan_thermal_anomaly(lat, lon):
    # ... (Keep existing code)
    pass