from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.sensor import SensorReadingDB
from typing import List
from datetime import datetime, timedelta

class HistoryService:

    async def get_trend(
        self,
        db: AsyncSession,
        asset_id: int,
        hours: int = 24
    ) -> List[SensorReadingDB]:
        since = datetime.now() - timedelta(hours=hours)
        result = await db.execute(
            select(SensorReadingDB)
            .where(
                SensorReadingDB.asset_id == asset_id,
                SensorReadingDB.timestamp >= since
            )
            .order_by(SensorReadingDB.timestamp.asc())
        )
        return result.scalars().all()

    async def get_summary(self, db: AsyncSession, asset_id: int, hours: int = 24):
        readings = await self.get_trend(db, asset_id, hours)
        if not readings:
            return {"min": 0, "max": 0, "avg": 0, "count": 0}

        values = [r.rms for r in readings]
        return {
            "min":   round(min(values), 3),
            "max":   round(max(values), 3),
            "avg":   round(sum(values) / len(values), 3),
            "count": len(values)
        }

history_service = HistoryService()