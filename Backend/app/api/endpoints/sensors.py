from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.models.sensor import RealtimeData
from app.services.sensor_service import sensor_service
from pydantic import BaseModel

router = APIRouter(prefix="/sensors", tags=["sensors"])

class SensorInput(BaseModel):
    asset_id: int
    rms:      float
    peak:     float = None

@router.post("/reading", response_model=RealtimeData)
async def post_reading(data: SensorInput, db: AsyncSession = Depends(get_db)):
    try:
        return await sensor_service.process_reading(db, data.asset_id, data.rms)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/realtime/{asset_id}", response_model=RealtimeData)
async def get_realtime(asset_id: int, db: AsyncSession = Depends(get_db)):
    from app.services.asset_service import asset_service
    asset = await asset_service.get_by_id(db, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return await sensor_service.process_reading(db, asset_id, asset.rms_actual)