from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.models.alarm import AlarmResponse, AlarmCreate
from app.services.alarm_service import alarm_service
from typing import List

router = APIRouter(prefix="/alarms", tags=["alarms"])

@router.get("/", response_model=List[AlarmResponse])
async def get_alarms(active_only: bool = False, db: AsyncSession = Depends(get_db)):
    return await alarm_service.get_all(db, only_active=active_only)

@router.get("/asset/{asset_id}", response_model=List[AlarmResponse])
async def get_alarms_by_asset(asset_id: int, db: AsyncSession = Depends(get_db)):
    return await alarm_service.get_by_asset(db, asset_id)

@router.post("/", response_model=AlarmResponse, status_code=201)
async def create_alarm(data: AlarmCreate, db: AsyncSession = Depends(get_db)):
    return await alarm_service.create(db, data)

@router.patch("/{alarm_id}/resolve", response_model=AlarmResponse)
async def resolve_alarm(alarm_id: int, db: AsyncSession = Depends(get_db)):
    alarm = await alarm_service.resolve(db, alarm_id)
    if not alarm:
        raise HTTPException(status_code=404, detail="Alarma no encontrada")
    return alarm