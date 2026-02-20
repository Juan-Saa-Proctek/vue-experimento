from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from app.db.database import Base
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class SensorReadingDB(Base):
    __tablename__ = "sensor_readings"

    id         = Column(Integer, primary_key=True, index=True)
    asset_id   = Column(Integer, ForeignKey("assets.id"), nullable=False, index=True)
    rms        = Column(Float, nullable=False)
    peak       = Column(Float, nullable=True)
    fft_data   = Column(Text, nullable=True)
    frequencies = Column(Text, nullable=True)
    timestamp  = Column(DateTime, server_default=func.now(), index=True)


class SensorReadingResponse(BaseModel):
    id:        int
    asset_id:  int
    rms:       float
    peak:      Optional[float] = None
    timestamp: datetime

    class Config:
        from_attributes = True


class RealtimeData(BaseModel):
    asset_id:    int
    rms:         float
    waveform:    List[float]
    fft_data:    List[float]
    frequencies: List[float]
    timestamp:   datetime


class HistoricalFFTResponse(BaseModel):
    asset_id:    int
    timestamp:   datetime
    rms:         float
    fft_data:    List[float]
    frequencies: List[float]