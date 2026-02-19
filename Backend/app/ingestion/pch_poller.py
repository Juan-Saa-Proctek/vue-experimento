"""
PCH Poller — consulta grabaciones del servidor PCH y las procesa
como lecturas de sensor en el sistema local.

Flujo:
1. Para cada activo local cuyo tag coincida con un dispositivo PCH
2. Consulta la última grabación del servidor PCH
3. Extrae RMS real desde totalRMS del waveform
4. Lo procesa por sensor_service → WebSocket → frontend
"""
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Optional
import numpy as np

from app.db.database import AsyncSessionLocal
from app.services.sensor_service import sensor_service
from app.services.asset_service import asset_service
from app.core.websocket import ws_manager
from app.core.config import settings
from app.integrations.pch_connection import PCHConnection

logger = logging.getLogger(__name__)


async def get_latest_recording(conn: PCHConnection, device_host_id: str, device_id: str):
    """Obtiene la grabación más reciente del dispositivo."""
    url = f"{conn.get_service_url('backend')}/timerecording/recordings"
    try:
        response = await conn.client.get(
            url,
            params={
                "session_token": conn.session_token,
                "deviceHostId":  device_host_id,
                "deviceId":      device_id,
                "start":         (datetime.now() - timedelta(days=7)).isoformat(),
                "end":           datetime.now().isoformat(),
            }
        )
        if response.status_code == 200:
            recordings = response.json()
            if recordings:
                recordings.sort(key=lambda r: r.get("date", ""), reverse=True)
                return recordings[0]
    except Exception as e:
        logger.error(f"Error obteniendo grabaciones de {device_id}: {e}")
    return None


async def get_waveform(conn: PCHConnection, recording_id: str, device_host_id: str, device_id: str):
    """Descarga el waveform raw del canal 1."""
    url = f"{conn.get_service_url('backend')}/timerecording/recording/channel/raw"
    try:
        response = await conn.client.get(
            url,
            params={
                "session_token": conn.session_token,
                "recordingId":   recording_id,
                "deviceHostId":  device_host_id,
                "deviceId":      device_id,
                "channel":       1,
            }
        )
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        logger.error(f"Error obteniendo waveform de {device_id}: {e}")
    return None


def extract_rms(recording: dict, waveform_data: Optional[dict] = None) -> float:
    """
    Extrae el RMS con prioridad:
    1. totalRMS del waveform (más preciso, calculado por el sensor)
    2. parameters[0].value de la grabación
    3. Calcular desde samples como fallback
    """
    # 1. totalRMS del waveform
    if waveform_data:
        total_rms = waveform_data.get("totalRMS")
        if total_rms and total_rms > 0:
            return float(total_rms)

        samples = waveform_data.get("samples", [])
        if samples:
            return float(np.sqrt(np.mean(np.array(samples) ** 2)))

    # 2. Parámetros de la grabación
    for param in recording.get("parameters", []):
        if param.get("value", 0) > 0:
            return float(param["value"])

    return 0.0


def subsample_waveform(samples: list, target: int = 200) -> list:
    """Submuestrea el waveform a N puntos para el frontend."""
    arr = np.array(samples)
    indices = np.linspace(0, len(arr) - 1, target, dtype=int)
    return arr[indices].tolist()


async def poll_device(conn: PCHConnection, asset_id: int, device_host_id: str, device_id: str):
    """Consulta y procesa un dispositivo PCH."""
    try:
        recording = await get_latest_recording(conn, device_host_id, device_id)
        if not recording:
            logger.warning(f"Sin grabaciones recientes para {device_id}")
            return

        recording_id  = recording.get("id")
        waveform_data = await get_waveform(conn, recording_id, device_host_id, device_id)
        rms           = extract_rms(recording, waveform_data)

        if rms == 0:
            logger.warning(f"RMS=0 para {device_id}, saltando")
            return

        async with AsyncSessionLocal() as db:
            result = await sensor_service.process_reading(db, asset_id, rms)

            # Reemplazar waveform simulado con el real
            if waveform_data and waveform_data.get("samples"):
                result.waveform = subsample_waveform(waveform_data["samples"])
                _, result.fft_data = sensor_service.generate_fft(result.waveform)

            await ws_manager.broadcast_to_asset(asset_id, result.model_dump(mode="json"))

        logger.info(f"PCH poll ✓ {device_id} | RMS={rms:.4f} | {recording.get('date', '')}")

    except Exception as e:
        logger.error(f"Error procesando {device_id}: {e}")


async def pch_poller():
    """
    Loop principal del poller PCH.
    El intervalo se lee de settings en cada ciclo — así el usuario
    puede cambiarlo desde Settings sin reiniciar el servidor.
    """
    logger.info("🔄 PCH poller iniciado")

    while True:
        interval_seconds = settings.PCH_INTERVAL_MINUTES * 60

        if not settings.PCH_ENABLED:
            await asyncio.sleep(60)
            continue

        conn = PCHConnection(
            host=settings.PCH_HOST,
            username=settings.PCH_USER,
            password=settings.PCH_PASSWORD,
        )

        try:
            ok = await conn.login()
            if not ok:
                logger.error("PCH poller: login fallido")
                await asyncio.sleep(interval_seconds)
                continue

            devices = await conn.get_device_list()
            if not devices:
                await asyncio.sleep(interval_seconds)
                continue

            # Mapa tag → device para matching con activos locales
            device_map = {
                f"{d['deviceHostId']}.{d['deviceId']}": d
                for d in devices
            }

            async with AsyncSessionLocal() as db:
                assets = await asset_service.get_all(db)

            for asset in assets:
                if asset.tag in device_map:
                    device = device_map[asset.tag]
                    await poll_device(
                        conn,
                        asset.id,
                        device["deviceHostId"],
                        device["deviceId"],
                    )
                    await asyncio.sleep(2)  # pausa entre dispositivos

        except Exception as e:
            logger.error(f"Error en PCH poller: {e}")
        finally:
            await conn.logout()

        logger.info(f"🔄 PCH poll completado. Próximo en {settings.PCH_INTERVAL_MINUTES} min.")
        await asyncio.sleep(interval_seconds)