from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class TurbineReading(Base):
    __tablename__ = "turbine_readings"

    id          = Column(Integer, primary_key=True, index=True)
    turbine_id  = Column(String(50), nullable=False)
    temperature = Column(Float, nullable=False)
    unit        = Column(String(10), default="celsius")
    status      = Column(String(20), nullable=False)  # normal / warning / critical
    timestamp   = Column(DateTime, default=datetime.now)

    alerts = relationship("TurbineAlert", back_populates="reading")


class TurbineAlert(Base):
    __tablename__ = "turbine_alerts"

    id          = Column(Integer, primary_key=True, index=True)
    reading_id  = Column(Integer, ForeignKey("turbine_readings.id"))
    turbine_id  = Column(String(50), nullable=False)
    severity    = Column(String(20), nullable=False)  # warning / critical
    temperature = Column(Float, nullable=False)
    message     = Column(String(255), nullable=False)
    created_at  = Column(DateTime, default=datetime.now)

    reading = relationship("TurbineReading", back_populates="alerts")
