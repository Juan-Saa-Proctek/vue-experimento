import asyncio
import json
import logging
import serial
import serial.tools.list_ports
from app.db.database import AsyncSessionLocal
from app.services.sensor_service import sensor_service
from app.core.websocket import ws_manager
from app.core.config import settings

logger = logging.getLogger(__name__)

class SerialReader:
    """
    Lee datos de un sensor conectado por Serial/UART.

    Formato esperado por línea (JSON):
    {"asset_id": 1, "rms": 2.5, "peak": 3.1}
    
    O formato CSV:
    1,2.5,3.1  (asset_id,rms,peak)
    """

    def __init__(self):
        self.running = False
        self.port    = None

    @staticmethod
    def list_ports():
        ports = serial.tools.list_ports.comports()
        return [p.device for p in ports]

    def parse_line(self, line: str) -> dict:
        line = line.strip()
        # Intenta JSON primero
        try:
            return json.loads(line)
        except json.JSONDecodeError:
            pass
        # Intenta CSV
        parts = line.split(",")
        if len(parts) >= 2:
            return {
                "asset_id": int(parts[0]),
                "rms":      float(parts[1]),
                "peak":     float(parts[2]) if len(parts) > 2 else None
            }
        raise ValueError(f"Formato no reconocido: {line}")

    async def process_line(self, data: dict):
        try:
            asset_id = int(data["asset_id"])
            rms      = float(data["rms"])

            async with AsyncSessionLocal() as db:
                result = await sensor_service.process_reading(db, asset_id, rms)
                await ws_manager.broadcast_to_asset(asset_id, result.model_dump(mode="json"))

            logger.info(f"Serial → Asset {asset_id} RMS={rms}")

        except Exception as e:
            logger.error(f"Error procesando línea serial: {e}")

    async def start(self, port: str = None, baudrate: int = None):
        port     = port     or settings.SERIAL_PORT
        baudrate = baudrate or settings.SERIAL_BAUDRATE

        if not port:
            logger.warning("Puerto serial no configurado, lector desactivado")
            return

        self.running = True
        logger.info(f"Abriendo puerto serial {port} @ {baudrate} baud")

        try:
            ser = serial.Serial(port, baudrate, timeout=1)
            loop = asyncio.get_event_loop()

            while self.running:
                line = await loop.run_in_executor(None, ser.readline)
                if line:
                    try:
                        decoded = line.decode("utf-8", errors="ignore")
                        data    = self.parse_line(decoded)
                        await self.process_line(data)
                    except Exception as e:
                        logger.warning(f"Línea serial inválida: {e}")

            ser.close()

        except serial.SerialException as e:
            logger.error(f"Error abriendo puerto serial {port}: {e}")

    def stop(self):
        self.running = False

serial_reader = SerialReader()