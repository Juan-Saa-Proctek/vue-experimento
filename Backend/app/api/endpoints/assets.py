from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.models.asset import AssetCreate, AssetUpdate, AssetResponse
from app.services.asset_service import asset_service
from typing import List

router = APIRouter(prefix="/assets", tags=["assets"])

@router.get("/", response_model=List[AssetResponse])
async def get_assets(db: AsyncSession = Depends(get_db)):
    return await asset_service.get_all(db)

@router.get("/{asset_id}", response_model=AssetResponse)
async def get_asset(asset_id: int, db: AsyncSession = Depends(get_db)):
    asset = await asset_service.get_by_id(db, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return asset

@router.post("/", response_model=AssetResponse, status_code=201)
async def create_asset(data: AssetCreate, db: AsyncSession = Depends(get_db)):
    existing = await asset_service.get_by_tag(db, data.tag)
    if existing:
        raise HTTPException(status_code=400, detail=f"Ya existe un equipo con el tag {data.tag}")
    return await asset_service.create(db, data)

@router.patch("/{asset_id}", response_model=AssetResponse)
async def update_asset(asset_id: int, data: AssetUpdate, db: AsyncSession = Depends(get_db)):
    asset = await asset_service.update(db, asset_id, data)
    if not asset:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return asset

@router.delete("/{asset_id}", status_code=204)
async def delete_asset(asset_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await asset_service.delete(db, asset_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")