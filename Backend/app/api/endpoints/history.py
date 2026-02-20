from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.models.sensor import SensorReadingResponse, HistoricalFFTResponse
from app.services.history_service import history_service
from typing import List
from datetime import datetime

router = APIRouter(prefix="/history", tags=["history"])


@router.get("/{asset_id}/trend", response_model=List[SensorReadingResponse])
async def get_trend(asset_id: int, hours: int = 24, limit: int = 1000,  db: AsyncSession = Depends(get_db)):
    return await history_service.get_trend(db, asset_id, hours, limit)  # 🔧 Pasar limit


@router.get("/{asset_id}/fft", response_model=HistoricalFFTResponse)
async def get_historical_fft(
    asset_id: int,
    timestamp: datetime,
    tolerance: int = 5,
    db: AsyncSession = Depends(get_db)
):
    result = await history_service.get_fft_at_timestamp(
        db, asset_id, timestamp, tolerance
    )
    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontró lectura para el asset {asset_id} en torno a {timestamp}"
        )
    return result


@router.get("/{asset_id}/summary")
async def get_summary(
    asset_id: int, 
    hours: int = 24, 
    db: AsyncSession = Depends(get_db)
):
    return await history_service.get_summary(db, asset_id, hours)