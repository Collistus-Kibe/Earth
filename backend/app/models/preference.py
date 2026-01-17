from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from .database import Base

class UserPreference(Base):
    __tablename__ = "user_preferences"

    # Link this to the user's UID from the 'users' table
    user_uid = Column(String(128), ForeignKey("users.uid"), primary_key=True)
    
    # Location Data
    home_latitude = Column(Float, nullable=True)
    home_longitude = Column(Float, nullable=True)
    default_zoom = Column(Integer, default=10, nullable=False)
    
    # Messaging Configuration
    fcm_device_token = Column(String(500), nullable=True)
    
    # Subscription Settings
    sub_weekly_digest = Column(Boolean, default=True)
    sub_astronomy_alerts = Column(Boolean, default=True) 
    
    # Tracking
    last_alert_sent_at = Column(DateTime(timezone=True), nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<UserPreference(user_uid='{self.user_uid}')>"