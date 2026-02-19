from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.database import Base
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AlarmDB(Base):
    __tablename__ = "alarms"

    id         = Column(Integer, primary_key=True, index=True)
    asset_id   = Column(Integer, ForeignKey("assets.id"), nullable=False)
    asset_tag  = Column(String, nullable=False)
    asset_name = Column(String, nullable=False)
    severity   = Column(String, nullable=False)  # warning | critical
    message    = Column(String, nullable=False)
    rms_value  = Column(Float, nullable=False)
    active     = Column(Boolean, default=True)
    timestamp  = Column(DateTime, server_default=func.now())


class AlarmResponse(BaseModel):
    id:         int
    asset_id:   int
    asset_tag:  str
    asset_name: str
    severity:   str
    message:    str
    rms_value:  float
    active:     bool
    timestamp:  datetime

    class Config:
        from_attributes = True

class AlarmCreate(BaseModel):
    asset_id:   int
    asset_tag:  str
    asset_name: str
    severity:   str
    message:    str
    rms_value:  float