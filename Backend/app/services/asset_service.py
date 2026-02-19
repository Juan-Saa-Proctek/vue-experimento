from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.models.asset import AssetDB, AssetCreate, AssetUpdate
from typing import List, Optional

class AssetService:

    async def get_all(self, db: AsyncSession) -> List[AssetDB]:
        result = await db.execute(select(AssetDB))
        return result.scalars().all()

    async def get_by_id(self, db: AsyncSession, asset_id: int) -> Optional[AssetDB]:
        result = await db.execute(select(AssetDB).where(AssetDB.id == asset_id))
        return result.scalar_one_or_none()

    async def get_by_tag(self, db: AsyncSession, tag: str) -> Optional[AssetDB]:
        result = await db.execute(select(AssetDB).where(AssetDB.tag == tag))
        return result.scalar_one_or_none()

    async def create(self, db: AsyncSession, data: AssetCreate) -> AssetDB:
        asset = AssetDB(**data.model_dump())
        db.add(asset)
        await db.commit()
        await db.refresh(asset)
        return asset

    async def update(self, db: AsyncSession, asset_id: int, data: AssetUpdate) -> Optional[AssetDB]:
        asset = await self.get_by_id(db, asset_id)
        if not asset:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(asset, key, value)
        await db.commit()
        await db.refresh(asset)
        return asset

    async def delete(self, db: AsyncSession, asset_id: int) -> bool:
        asset = await self.get_by_id(db, asset_id)
        if not asset:
            return False
        await db.delete(asset)
        await db.commit()
        return True

    async def update_status(self, db: AsyncSession, asset_id: int, status: str, rms: float) -> Optional[AssetDB]:
        asset = await self.get_by_id(db, asset_id)
        if not asset:
            return None
        asset.status = status
        asset.rms_actual = rms
        await db.commit()
        await db.refresh(asset)
        return asset

asset_service = AssetService()