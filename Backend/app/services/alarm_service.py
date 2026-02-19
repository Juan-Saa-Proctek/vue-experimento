from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.alarm import AlarmDB, AlarmCreate
from typing import List, Optional

class AlarmService:

    async def get_all(self, db: AsyncSession, only_active: bool = False) -> List[AlarmDB]:
        query = select(AlarmDB).order_by(AlarmDB.timestamp.desc())
        if only_active:
            query = query.where(AlarmDB.active == True)
        result = await db.execute(query)
        return result.scalars().all()

    async def get_by_asset(self, db: AsyncSession, asset_id: int) -> List[AlarmDB]:
        result = await db.execute(
            select(AlarmDB)
            .where(AlarmDB.asset_id == asset_id)
            .order_by(AlarmDB.timestamp.desc())
        )
        return result.scalars().all()

    async def create(self, db: AsyncSession, data: AlarmCreate) -> AlarmDB:
        alarm = AlarmDB(**data.model_dump())
        db.add(alarm)
        await db.commit()
        await db.refresh(alarm)
        return alarm

    async def create_if_not_active(self, db: AsyncSession, data: AlarmCreate) -> Optional[AlarmDB]:
        existing = await self.get_active_by_asset_severity(
            db, data.asset_id, data.severity
        )
        if existing:
            return existing  # Ya existe, no duplicar
        return await self.create(db, data)

    async def get_active_by_asset_severity(self, db: AsyncSession, asset_id: int, severity: str) -> Optional[AlarmDB]:
        result = await db.execute(
            select(AlarmDB).where(
                AlarmDB.asset_id == asset_id,
                AlarmDB.severity == severity,
                AlarmDB.active == True,
            )
        )
        return result.scalar_one_or_none()

    async def resolve(self, db: AsyncSession, alarm_id: int) -> Optional[AlarmDB]:
        result = await db.execute(select(AlarmDB).where(AlarmDB.id == alarm_id))
        alarm = result.scalar_one_or_none()
        if not alarm:
            return None
        alarm.active = False
        await db.commit()
        await db.refresh(alarm)
        return alarm

    async def resolve_by_asset(self, db: AsyncSession, asset_id: int):
        result = await db.execute(
            select(AlarmDB)
            .where(AlarmDB.asset_id == asset_id, AlarmDB.active == True)
        )
        alarms = result.scalars().all()
        for alarm in alarms:
            alarm.active = False
        await db.commit()

alarm_service = AlarmService()