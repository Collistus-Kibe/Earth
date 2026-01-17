import os
import google.generativeai as genai
# Import the new Air Quality service
from app.services import open_meteo, space, air_quality

GEMINI_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)

async def generate_daily_briefing(lat: float, lon: float, user_name: str = "Friend"):
    try:
        # 1. GATHER ALL INTEL
        weather = await open_meteo.get_raw_weather_data(lat, lon)
        air = await air_quality.get_pollution_levels(lat, lon) # <-- NEW
        
    except Exception as e:
        return "Systems initializing. Stand by."

    # 2. THE HERO PROMPT
    prompt = f"""
    Role: You are 'EARTH', a sentient planetary guardian. You care deeply about nature and human survival.
    
    Current Data for {user_name}:
    - Carbon Monoxide (Emissions): {air.co} µg/m³
    - Air Status: {air.status}
    - Temperature: {weather.temp_max}°C
    - Rain Forecast: {weather.precipitation}mm
    
    INSTRUCTIONS:
    Write a short, 2-sentence message to the user.
    
    LOGIC:
    1. IF Carbon Monoxide is HIGH (> 300) or Status is 'Polluted': 
       - Tone: Sad/Urgent.
       - Message: "Bad news today. High carbon emissions are choking the air. Try to use public transport or plant a tree to help me breathe."
       
    2. IF Carbon Monoxide is LOW (< 150) and Status is 'Clean':
       - Tone: Happy/Proud.
       - Message: "Good news! The air is crisp and carbon levels are low. Thank you for keeping the planet healthy today."
       
    3. IF Rain is High (> 20mm):
       - Tone: Protective.
       - Message: "I am watering the earth today with heavy rain. Please stay dry and avoid flood zones."

    Keep it under 40 words. Be personal.
    """

    if not GEMINI_KEY:
        # Fallback Logic if no API Key
        if air.co > 300: return f"High carbon levels detected. Please reduce emissions today, {user_name}."
        if weather.precipitation > 10: return f"Heavy rain expected. Stay safe and keep warm, {user_name}."
        return f"Air quality is excellent today. A perfect day to enjoy nature, {user_name}."

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        return "Monitoring Earth's vitals. Systems nominal."