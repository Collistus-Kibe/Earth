import numpy as np
import pandas as pd
from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import date, timedelta
import random

# --- Scikit-Learn Imports ---
from sklearn.linear_model import LinearRegression

# --- Pydantic Import (THE FIX) ---
from pydantic import BaseModel

# --- Import Models ---
from app.models.history import RegionalHistory

# --- UPDATED CLASS DEFINITION ---
class TrendPrediction(BaseModel):
    direction: str      # "Increasing", "Decreasing", "Stable"
    slope: float        # The steepness of the trend
    next_week_score: float # Predicted score 7 days from now
    confidence: str     # "High" (lots of data) vs "Low" (little data)
    message: str

def generate_mock_history(db: Session, lat: float, lon: float):
    """
    COLD START HELPER:
    Generates 30 days of synthetic historical data for a location.
    """
    existing = db.query(RegionalHistory).filter(
        RegionalHistory.latitude == lat, 
        RegionalHistory.longitude == lon
    ).first()
    
    if existing:
        return # Data already exists
        
    print(f"Generating 30-day mock history for {lat}, {lon}...")
    
    today = date.today()
    base_soil = 0.2
    base_risk = 10.0
    
    for i in range(30, 0, -1):
        day = today - timedelta(days=i)
        
        # Simulate a "worsening" trend for the demo
        daily_rain = random.uniform(0, 10) + (30 - i) * 0.5
        soil_moisture = min(0.5, base_soil + (30 - i) * 0.01)
        daily_risk = min(100, base_risk + (daily_rain * 2) + (soil_moisture * 50))
        
        record = RegionalHistory(
            latitude=lat,
            longitude=lon,
            date=day,
            avg_temp_c=25.0 + random.uniform(-2, 2),
            precipitation_mm=daily_rain,
            soil_moisture_index=soil_moisture,
            calculated_flood_risk=daily_risk,
            calculated_fire_risk=max(0, 80 - daily_risk)
        )
        db.add(record)
    
    db.commit()
    print("Mock history generated.")


def predict_flood_trend(db: Session, lat: float, lon: float) -> TrendPrediction:
    """
    Uses Linear Regression to analyze the last 30 days of flood risk.
    """
    # 1. Fetch Data
    history = db.query(RegionalHistory).filter(
        RegionalHistory.latitude == lat,
        RegionalHistory.longitude == lon
    ).order_by(RegionalHistory.date).all()
    
    if len(history) < 5:
        return TrendPrediction(
            direction="Unknown", 
            slope=0.0, 
            next_week_score=0.0, 
            confidence="None", 
            message="Not enough historical data to predict trends."
        )
        
    # 2. Prepare Data
    df = pd.DataFrame([{
        "day_index": (r.date - history[0].date).days,
        "risk": r.calculated_flood_risk
    } for r in history])
    
    X = df[["day_index"]]
    y = df["risk"]
    
    # 3. Train Model
    model = LinearRegression()
    model.fit(X, y)
    
    slope = model.coef_[0]
    
    # 4. Predict Future
    last_day_index = df["day_index"].max()
    future_day_index = last_day_index + 7
    predicted_risk = model.predict([[future_day_index]])[0]
    
    # 5. Interpret Results
    direction = "Stable"
    if slope > 0.5:
        direction = "Increasing Quickly"
    elif slope > 0.1:
        direction = "Increasing Slowly"
    elif slope < -0.5:
        direction = "Decreasing Quickly"
    elif slope < -0.1:
        direction = "Decreasing Slowly"
        
    predicted_risk = max(0, min(100, predicted_risk))
    
    msg = f"Flood risk is {direction.lower()}. "
    if slope > 0:
        msg += f"Based on the last 30 days, risk is trending UP by {round(slope, 2)} points per day."
    else:
        msg += "Conditions are improving."

    # This was the line causing the crash. Now it works because TrendPrediction is a BaseModel.
    return TrendPrediction(
        direction=direction,
        slope=slope,
        next_week_score=round(predicted_risk, 1),
        confidence="High" if len(history) > 20 else "Medium",
        message=msg
    )