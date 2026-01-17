import os
from openai import AsyncOpenAI
from fastapi import HTTPException
from pydantic import BaseModel

# --- Initialize OpenAI Client ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    print("CRITICAL: OPENAI_API_KEY not set. AI Report will fail.")
    client = None
else:
    try:
        client = AsyncOpenAI(api_key=OPENAI_API_KEY)
        print("OpenAI client initialized.")
    except Exception as e:
        print(f"CRITICAL: Failed to initialize OpenAI: {e}")
        client = None

# --- NEW: Pydantic model for our local data ---
class LocalSummaryData(BaseModel):
    safety_score: int
    primary_risk: str
    aqi: int | None
    temperature: float
    fire_risk: int

async def get_local_insight(summary: LocalSummaryData) -> str:
    """
    Generates a high-level LOCAL insight using the OpenAI API based on
    the user's complete local intelligence summary.
    """
    if not client:
        raise HTTPException(status_code=500, detail="OpenAI service is not configured.")

    # This prompt is now much smarter and more personal
    prompt = f"""
    You are an expert risk analyst for the 'EARTH' platform.
    A user's local intelligence summary is as follows:
    - Overall Safety Score: {summary.safety_score}/100 (100 is safe, 0 is dangerous)
    - Primary Risk Factor: "{summary.primary_risk}"
    - Air Quality Index (AQI): {summary.aqi or 'N/A'}
    - Max Temperature: {summary.temperature}°C
    - Fire Risk Score: {summary.fire_risk}/100

    Write a single, concise, and helpful sentence (max 30 words) for the user.
    If the risk is high, be direct. If it's low, be reassuring.
    
    Example (High Risk): "Your personal safety score is very low due to extreme fire risk; avoid outdoor activity and stay alert."
    Example (Low Risk): "Your local conditions are stable, with a high safety score and no immediate environmental risks detected."
    Example (AQI Risk): "Your safety score is moderate; while fire risk is low, be mindful of poor air quality today."
    """

    try:
        chat_completion = await client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": prompt,
                }
            ],
            model="gpt-3.5-turbo",
            max_tokens=60,
            temperature=0.7
        )
        
        if chat_completion.choices:
            return chat_completion.choices[0].message.content.strip()
        else:
            return "No insight could be generated at this time."
            
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        raise HTTPException(status_code=503, detail=f"AI service request failed: {e}")