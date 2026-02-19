from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.db.database import Base
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Modelo SQLAlchemy (tabla en DB)
class AssetDB(Base):
    __tablename__ = "assets"

    id           = Column(Integer, primary_key=True, index=True)
    tag          = Column(String, unique=True, index=True, nullable=False)
    name         = Column(String, nullable=False)
    type         = Column(String, nullable=False)
    location     = Column(String)
    rpm_nominal  = Column(Float, default=0)
    rms_limit    = Column(Float, default=4.5)
    status       = Column(String, default="offline")
    rms_actual   = Column(Float, default=0)
    created_at   = Column(DateTime, server_default=func.now())
    updated_at   = Column(DateTime, server_default=func.now(), onupdate=func.now())


# Esquemas Pydantic (validación y serialización)
class AssetBase(BaseModel):
    tag:         str
    name:        str
    type:        str
    location:    Optional[str] = None
    rpm_nominal: float = 0
    rms_limit:   float = 4.5

class AssetCreate(AssetBase):
    pass

class AssetUpdate(BaseModel):
    name:        Optional[str] = None
    type:        Optional[str] = None
    location:    Optional[str] = None
    rpm_nominal: Optional[float] = None
    rms_limit:   Optional[float] = None
    status:      Optional[str] = None
    rms_actual:  Optional[float] = None

class AssetResponse(AssetBase):
    id:         int
    status:     str
    rms_actual: float
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True