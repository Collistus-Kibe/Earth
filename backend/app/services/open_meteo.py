import httpx
import json
import os
import time
from datetime import datetime, timedelta

CACHE_FILE = "weather_cache.json"
CACHE_DURATION = 3600

# --- 1. WEATHER & UV (Used by Infra & Dashboard) ---
async def get_raw_weather_data(lat: float, lon: float):
    cached = load_from_cache(f"raw_{lat}_{lon}")
    if cached: return cached

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": lat, "longitude": lon,
                    "daily": ["temperature_2m_max", "uv_index_max", "precipitation_sum", "wind_speed_10m_max"],
                    "current": ["temperature_2m", "relative_humidity_2m"],
                    "timezone": "auto"
                }, timeout=30.0
            )
            response.raise_for_status()
            data = response.json()
            result = parse_weather_data(data)
            save_to_cache(f"raw_{lat}_{lon}", result)
            return result
        except Exception as e:
            print(f"Weather API Error: {e}")
            raise e

# --- 2. FLOOD DATA (Used by Infra & Bio) ---
async def get_flood_data(lat: float, lon: float):
    cached = load_from_cache(f"flood_{lat}_{lon}")
    if cached: return cached

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": lat, "longitude": lon,
                    "hourly": ["soil_moisture_0_to_7cm"],
                    "daily": ["precipitation_sum"],
                    "timezone": "auto"
                }, timeout=30.0
            )
            data = response.json()
            
            soil = data.get("hourly", {}).get("soil_moisture_0_to_7cm", [0])[0]
            rain = sum(data.get("daily", {}).get("precipitation_sum", []))
            
            result = type('obj', (object,), {
                "precipitation_forecast_7d": rain,
                "soil_moisture_current": soil,
                "uv_index_tomorrow": 5
            })
            save_to_cache(f"flood_{lat}_{lon}", result)
            return result
        except:
            return type('obj', (object,), {"precipitation_forecast_7d": 0, "soil_moisture_current": 0.2})

# --- 3. MARINE / OCEAN DATA (New for Math) ---
async def get_marine_data(lat: float, lon: float):
    cached = load_from_cache(f"marine_{lat}_{lon}")
    if cached: return cached

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                "https://marine-api.open-meteo.com/v1/marine",
                params={
                    "latitude": lat, "longitude": lon,
                    "current": ["wave_height", "wave_direction", "wave_period"],
                    "daily": ["wave_height_max"],
                    "timezone": "auto"
                }, timeout=30.0
            )
            return response.json()
        except:
            return {}

# --- 4. AIR QUALITY ---
async def get_air_quality(lat: float, lon: float):
    cached = load_from_cache(f"air_{lat}_{lon}")
    if cached: return cached

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                "https://air-quality-api.open-meteo.com/v1/air-quality",
                params={
                    "latitude": lat, "longitude": lon,
                    "current": ["us_aqi", "dust"],
                    "timezone": "auto"
                }, timeout=30.0
            )
            result = response.json()
            save_to_cache(f"air_{lat}_{lon}", result)
            return result
        except:
            return {"current": {"us_aqi": 42}}

# --- 5. FORECAST JSON ---
async def get_7_day_forecast(lat: float, lon: float):
    cached = load_from_cache(f"forecast_{lat}_{lon}")
    if cached: return cached

    async with httpx.AsyncClient() as client:
        try:
            res = await client.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": lat, "longitude": lon,
                    "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum"],
                    "timezone": "auto"
                }, timeout=30.0
            )
            data = res.json()
            save_to_cache(f"forecast_{lat}_{lon}", data)
            return data
        except: return {}

# --- 6. HISTORY ---
async def get_historical_weather(lat: float, lon: float, days: int = 10):
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("https://archive-api.open-meteo.com/v1/archive", params={
                "latitude": lat, "longitude": lon,
                "start_date": start_date, "end_date": end_date,
                "daily": ["precipitation_sum"],
                "timezone": "auto"
            })
            return response.json()
        except:
            return {}

# --- HELPER FUNCTIONS (SYNTAX FIXED) ---

def save_to_cache(key, data):
    full_cache = {}
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r') as f:
                full_cache = json.load(f)
        except:
            pass
    
    if hasattr(data, '__dict__'):
        serialized = data.__dict__
    elif hasattr(data, 'precipitation_forecast_7d'):
        serialized = {
            "precipitation_forecast_7d": data.precipitation_forecast_7d,
            "soil_moisture_current": data.soil_moisture_current,
            "uv_index_tomorrow": 5
        }
    else:
        serialized = data

    full_cache[key] = {"timestamp": time.time(), "data": serialized}
    
    try:
        with open(CACHE_FILE, 'w') as f:
            json.dump(full_cache, f)
    except:
        pass

def load_from_cache(key):
    if not os.path.exists(CACHE_FILE):
        return None
    try:
        with open(CACHE_FILE, 'r') as f:
            full_cache = json.load(f)
        
        if key not in full_cache:
            return None
            
        if time.time() - full_cache[key]["timestamp"] < CACHE_DURATION:
            data = full_cache[key]["data"]
            
            if "temp_max" in data: 
                class WeatherData:
                    def __init__(self, d): self.__dict__.update(d)
                return WeatherData(data)
            
            if "soil_moisture_current" in data:
                return type('obj', (object,), data)
            
            return data
    except:
        return None
    return None

def parse_weather_data(data):
    class WeatherData:
        def __init__(self, d):
            daily = d.get("daily", {})
            current = d.get("current", {})
            self.temp_max = daily.get("temperature_2m_max", [0])[0]
            self.temp_min = daily.get("temperature_2m_min", [0])[0]
            self.precipitation = daily.get("precipitation_sum", [0])[0]
            self.wind_max = daily.get("wind_speed_10m_max", [0])[0]
            self.humidity_min = current.get("relative_humidity_2m", 0)
            self.uv_index = daily.get("uv_index_max", [0])[0]
    return WeatherData(data)