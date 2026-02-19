from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.models.sensor import SensorReadingResponse
from app.services.history_service import history_service
from typing import List

router = APIRouter(prefix="/history", tags=["history"])

@router.get("/{asset_id}/trend", response_model=List[SensorReadingResponse])
async def get_trend(asset_id: int, hours: int = 24, db: AsyncSession = Depends(get_db)):
    return await history_service.get_trend(db, asset_id, hours)

@router.get("/{asset_id}/summary")
async def get_summary(asset_id: int, hours: int = 24, db: AsyncSession = Depends(get_db)):
    return await history_service.get_summary(db, asset_id, hours)