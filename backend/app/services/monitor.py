from sqlalchemy.orm import Session
from datetime import datetime
from app.models.preference import UserPreference
from app.models.history import RegionalHistory
from app.services import messaging

# Import our intelligence services
from app.services import open_meteo, space
from app import processing

async def run_daily_check_for_user(user_uid: str, db: Session):
    """
    This function runs the intelligence logic for a single user
    and triggers the appropriate messages.
    """
    # 1. Get User Preferences
    prefs = db.query(UserPreference).filter(UserPreference.user_uid == user_uid).first()
    if not prefs or not prefs.fcm_device_token:
        print(f"User {user_uid} has no location or no FCM token. Skipping.")
        return

    lat, lon = prefs.home_latitude, prefs.home_longitude
    token = prefs.fcm_device_token
    
    print(f"Running Monitor for User {user_uid} at {lat}, {lon}...")

    # --- CHECK 1: MANDATORY DISASTER CHECKS (The Guardian) ---
    # We always check this, regardless of settings.
    
    # Check Flood Risk
    flood_data = await open_meteo.get_flood_data(lat, lon)
    # (Assuming rivers_data is loaded in app state, strictly we'd need to pass it here)
    # For this snippet, we use a simplified check based on raw rain for speed
    if flood_data.precipitation_forecast_7d > 100:
        messaging.send_disaster_alert(
            token, 
            "Flood Risk", 
            f"Heavy rain detected ({flood_data.precipitation_forecast_7d}mm). Flood risk is CRITICAL."
        )
        return # Don't send "good news" if we just sent a disaster alert!

    # --- CHECK 2: "GOOD INFO" (The Guide) ---
    
    # A. Astronomy Check (If Subscribed)
    if prefs.sub_astronomy_alerts:
        space_data = await space.get_space_weather()
        # Example: If there is a Solar Flare, tell them (it's interesting!) 
        # Or if conditions are calm, suggest stargazing.
        if "Low" in space_data.solar_risk_level:
             # Check for clear skies tonight (simplified)
             weather = await open_meteo.get_raw_weather_data(lat, lon)
             # Assuming cloud_cover logic exists, or low rain
             if weather.precipitation == 0:
                 messaging.send_good_news(
                     token,
                     "astronomy",
                     "Perfect Stargazing Tonight! Skies are clear and solar activity is low."
                 )

    # B. Weekly Digest (If Subscribed & If it's Monday)
    if prefs.sub_weekly_digest and datetime.now().weekday() == 0: # 0 = Monday
        weather = await open_meteo.get_7_day_forecast(lat, lon)
        avg_temp = sum([d.temp_max for d in weather.daily]) / 7
        messaging.send_good_news(
            token,
            "weather",
            f"Your Weekly Brief: Expect an average of {round(avg_temp)}°C this week. Have a great one!"
        )
    
    print(f"Monitor check complete for {user_uid}.")