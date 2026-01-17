from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base

class PollutantSource(Base):
    __tablename__ = "pollutant_sources"

    id = Column(String(36), primary_key=True, index=True) # A unique ID, e.g., UUID
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    
    # Optional: A user-provided description
    description = Column(String(500), nullable=True)
    
    # Link this report to the user who submitted it
    submitted_by_uid = Column(String(128), ForeignKey("users.uid"), nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Establish the relationship to the User model (optional but good practice)
    submitter = relationship("User")

    def __repr__(self):
        return f"<PollutantSource(lat={self.latitude}, lon={self.longitude})>"