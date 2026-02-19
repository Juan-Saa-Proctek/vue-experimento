import asyncio
import logging
from datetime import datetime, timedelta
from sqlalchemy import select
from app.db.database import AsyncSessionLocal
from app.models.sensor import SensorReadingDB
from app.models.asset import AssetDB
from app.core.websocket import ws_manager

logger = logging.getLogger(__name__)

# Tiempo sin lectura para considerar un activo offline
OFFLINE_TIMEOUT_SECONDS = 30


async def check_offline_assets():
    threshold = datetime.now() - timedelta(seconds=OFFLINE_TIMEOUT_SECONDS)

    async with AsyncSessionLocal() as db:
        # Obtener todos los activos que NO están ya offline
        result = await db.execute(
            select(AssetDB).where(AssetDB.status != "offline")
        )
        active_assets = result.scalars().all()

        for asset in active_assets:
            # Buscar la lectura más reciente del activo
            last_reading = await db.execute(
                select(SensorReadingDB)
                .where(SensorReadingDB.asset_id == asset.id)
                .order_by(SensorReadingDB.timestamp.desc())
                .limit(1)
            )
            reading = last_reading.scalar_one_or_none()

            # Si no hay lectura reciente, marcar offline
            if reading is None or reading.timestamp < threshold:
                asset.status = "offline"
                logger.info(
                    f"Asset {asset.tag} marcado offline "
                    f"(última lectura: {reading.timestamp if reading else 'nunca'})"
                )
                # Notificar al frontend por WebSocket
                await ws_manager.broadcast_to_asset(asset.id, {
                    "asset_id": asset.id,
                    "status": "offline",
                    "rms": 0.0,
                    "waveform": [],
                    "fft_data": [],
                    "frequencies": [],
                    "timestamp": datetime.now().isoformat(),
                })

        await db.commit()


async def offline_watcher(interval_seconds: int = 10):
    """
    Loop que ejecuta la verificación de assets offline periódicamente.
    Se inicia como tarea de fondo en el startup de la app.
    """
    logger.info(
        f"Offline watcher iniciado "
        f"(timeout={OFFLINE_TIMEOUT_SECONDS}s, intervalo={interval_seconds}s)"
    )
    while True:
        try:
            await check_offline_assets()
        except Exception as e:
            logger.error(f"Error en offline_watcher: {e}")
        await asyncio.sleep(interval_seconds)