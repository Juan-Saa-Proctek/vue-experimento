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