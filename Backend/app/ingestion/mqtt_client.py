import asyncio
import json
import logging
from typing import Optional
import aiomqtt
from app.core.config import settings
from app.db.database import AsyncSessionLocal
from app.services.sensor_service import sensor_service
from app.core.websocket import ws_manager

logger = logging.getLogger(__name__)

class MQTTClient:
    """
    Escucha tópicos MQTT y normaliza los datos al sensor_service.
    
    Tópico esperado: vibmonitor/assets/{asset_id}/reading
    Payload esperado: {"rms": 2.5, "peak": 3.1}
    """

    def __init__(self):
        self.running = False
        self.client  = None

    async def process_message(self, topic: str, payload: dict):
        try:
            # Extrae asset_id del tópico
            # Formato: vibmonitor/assets/1/reading
            parts    = topic.split("/")
            asset_id = int(parts[2])
            rms      = float(payload.get("rms", 0))

            async with AsyncSessionLocal() as db:
                result = await sensor_service.process_reading(db, asset_id, rms)
                # Transmite por WebSocket al frontend
                await ws_manager.broadcast_to_asset(asset_id, result.model_dump(mode="json"))

            logger.info(f"MQTT → Asset {asset_id} RMS={rms}")

        except Exception as e:
            logger.error(f"Error procesando mensaje MQTT: {e}")

    async def start(self):
        self.running = True
        logger.info(f"Conectando a MQTT broker {settings.MQTT_HOST}:{settings.MQTT_PORT}")
        try:
            async with aiomqtt.Client(
                hostname=settings.MQTT_HOST,
                port=settings.MQTT_PORT,
                username=settings.MQTT_USER or None,
                password=settings.MQTT_PASSWORD or None,
            ) as client:
                self.client = client
                await client.subscribe("vibmonitor/assets/+/reading")
                logger.info("MQTT suscrito a vibmonitor/assets/+/reading")
                async for message in client.messages:
                    if not self.running:
                        break
                    try:
                        payload = json.loads(message.payload.decode())
                        await self.process_message(str(message.topic), payload)
                    except json.JSONDecodeError:
                        logger.warning(f"Payload MQTT inválido: {message.payload}")
        except Exception as e:
            logger.error(f"Error MQTT: {e}")

    def stop(self):
        self.running = False

mqtt_client = MQTTClient()