from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.sensor import SensorReadingDB, RealtimeData
from app.models.alarm import AlarmCreate
from app.services.alarm_service import alarm_service
from app.services.asset_service import asset_service
from datetime import datetime
from typing import List, Optional
import numpy as np
import json

class SensorService:

    def compute_status(self, rms: float, rms_limit: float) -> str:
        if rms == 0:
            return "offline"
        warning_limit = rms_limit * 0.7
        if rms >= rms_limit:
            return "critical"
        elif rms >= warning_limit:
            return "warning"
        return "normal"

    def generate_waveform(self, rms: float, n_samples: int = 200) -> List[float]:
        t = np.linspace(0, 1, n_samples)
        signal = rms * np.sin(2 * np.pi * 29 * t)
        noise = np.random.normal(0, rms * 0.1, n_samples)
        return (signal + noise).tolist()

    def generate_fft(self, waveform: List[float], sample_rate: int = 1000):
        signal = np.array(waveform)
        n = len(signal)
        fft_vals = np.abs(np.fft.rfft(signal)) / n
        freqs = np.fft.rfftfreq(n, 1 / sample_rate)
        return freqs.tolist(), fft_vals.tolist()

    async def process_reading(self, db: AsyncSession, asset_id: int, rms: float) -> RealtimeData:
        asset = await asset_service.get_by_id(db, asset_id)
        if not asset:
            raise ValueError(f"Activo {asset_id} no encontrado")

        status = self.compute_status(rms, asset.rms_limit)
        await asset_service.update_status(db, asset_id, status, rms)

        # Generar waveform y FFT antes de guardar
        waveform = self.generate_waveform(rms)
        frequencies, fft_data = self.generate_fft(waveform)

        # Guardar lectura en historial incluyendo FFT serializado
        reading = SensorReadingDB(
            asset_id=asset_id,
            rms=rms,
            fft_data=json.dumps(fft_data),
            frequencies=json.dumps(frequencies),
        )
        db.add(reading)
        await db.commit()
        await db.refresh(reading)

        # Generar alarma solo si no existe ya una activa del mismo tipo
        if status in ("warning", "critical"):
            await alarm_service.create_if_not_active(db, AlarmCreate(
                asset_id=asset_id,
                asset_tag=asset.tag,
                asset_name=asset.name,
                severity=status,
                message=f"Vibración RMS {'supera el límite crítico' if status == 'critical' else 'en zona de advertencia'}",
                rms_value=rms
            ))
        elif status == "normal":
            await alarm_service.resolve_by_asset(db, asset_id)

        return RealtimeData(
            asset_id=asset_id,
            rms=rms,
            waveform=waveform,
            fft_data=fft_data,
            frequencies=frequencies,
            timestamp=datetime.now()
        )

sensor_service = SensorService()