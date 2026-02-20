from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.sensor import SensorReadingDB, HistoricalFFTResponse
from typing import List, Optional
from datetime import datetime, timedelta
import json
import numpy as np


def _regenerate_fft(rms: float):
    """Regenera FFT a partir del RMS si no está almacenada (lecturas antiguas)."""
    n_samples = 200
    t = np.linspace(0, 1, n_samples)
    signal = rms * np.sin(2 * np.pi * 29 * t)
    noise = np.random.normal(0, rms * 0.1, n_samples)
    waveform = signal + noise

    n = len(waveform)
    fft_vals = np.abs(np.fft.rfft(waveform)) / n
    freqs = np.fft.rfftfreq(n, 1 / 1000)
    return freqs.tolist(), fft_vals.tolist()


class HistoryService:

    async def get_trend(self,db: AsyncSession,asset_id: int,hours: int = 24,limit: int = 1000) -> List[SensorReadingDB]:
        since = datetime.now() - timedelta(hours=hours)
        
        result = await db.execute(
            select(SensorReadingDB)
            .where(
                SensorReadingDB.asset_id == asset_id,
                SensorReadingDB.timestamp >= since
            )
            .order_by(SensorReadingDB.timestamp.desc())  
            .limit(limit)  
        )
        
        readings = result.scalars().all()
        
        return list(reversed(readings))

    async def get_fft_at_timestamp(self, db: AsyncSession, asset_id: int, timestamp: datetime, tolerance_seconds: int = 5) -> Optional[HistoricalFFTResponse]:
  
        since = timestamp - timedelta(seconds=tolerance_seconds)
        until = timestamp + timedelta(seconds=tolerance_seconds)

        result = await db.execute(
            select(SensorReadingDB)
            .where(
                SensorReadingDB.asset_id == asset_id,
                SensorReadingDB.timestamp >= since,
                SensorReadingDB.timestamp <= until,
            )
            .order_by(SensorReadingDB.timestamp.desc())
            .limit(1)
        )
        reading = result.scalar_one_or_none()

        if not reading:
            return None

        # Usar FFT almacenada o regenerar
        if reading.fft_data and reading.frequencies:
            fft_data = json.loads(reading.fft_data)
            frequencies = json.loads(reading.frequencies)
        else:
            frequencies, fft_data = _regenerate_fft(reading.rms)

        return HistoricalFFTResponse(
            asset_id=asset_id,
            timestamp=reading.timestamp,
            rms=reading.rms,
            fft_data=fft_data,
            frequencies=frequencies,
        )

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