from sqlalchemy import Column, Integer, Float, Date, String
from sqlalchemy.sql import func
from .database import Base

class RegionalHistory(Base):
    __tablename__ = "regional_history"

    id = Column(Integer, primary_key=True, index=True)
    
    # Location indexing (Grid-based history)
    latitude = Column(Float, nullable=False, index=True)
    longitude = Column(Float, nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)

    # --- The Features (Inputs for AI) ---
    avg_temp_c = Column(Float)          # Daily Average Temp
    precipitation_mm = Column(Float)    # Daily Rain Sum
    soil_moisture_index = Column(Float) # Deep Soil Moisture (0.0 - 1.0)
    sea_surface_temp_c = Column(Float, nullable=True) # Null for land
    
    # --- The Targets (Labels for AI) ---
    # We store what the risk score *was* on that day.
    # The AI learns the trend of these scores over time.
    calculated_flood_risk = Column(Float) 
    calculated_fire_risk = Column(Float)

    def __repr__(self):
        return f"<History({self.date} @ {self.latitude},{self.longitude})>"