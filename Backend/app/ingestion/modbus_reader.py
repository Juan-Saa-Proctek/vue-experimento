import asyncio
import logging
from pymodbus.client import AsyncModbusTcpClient, AsyncModbusSerialClient
from app.db.database import AsyncSessionLocal
from app.services.sensor_service import sensor_service
from app.core.websocket import ws_manager
from app.core.config import settings

logger = logging.getLogger(__name__)

class ModbusReader:
    """
    Lee registros Modbus y los mapea a activos.

    Configuración de registros (ejemplo):
    Registro 0 → RMS del asset_id 1
    Registro 1 → Peak del asset_id 1
    Registro 2 → RMS del asset_id 2
    ...
    """

    def __init__(self):
        self.running = False
        self.client  = None
        # Mapeo: registro Modbus → asset_id
        # Configurable desde settings o DB en el futuro
        self.register_map = {
            0: {"asset_id": 1, "field": "rms"},
            1: {"asset_id": 1, "field": "peak"},
            2: {"asset_id": 2, "field": "rms"},
        }

    async def read_registers(self) -> dict:
        readings = {}
        try:
            result = await self.client.read_holding_registers(
                address=0,
                count=len(self.register_map)
            )
            if result.isError():
                logger.error("Error leyendo registros Modbus")
                return {}

            for reg_index, config in self.register_map.items():
                raw_value = result.registers[reg_index]
                # Convierte de entero a float (escala 0-10000 → 0.0-10.0 mm/s)
                value = raw_value / 1000.0
                asset_id = config["asset_id"]
                field    = config["field"]
                if asset_id not in readings:
                    readings[asset_id] = {}
                readings[asset_id][field] = value

        except Exception as e:
            logger.error(f"Error Modbus: {e}")

        return readings

    async def poll_loop(self, interval: float = 1.0):
        while self.running:
            readings = await self.read_registers()
            for asset_id, data in readings.items():
                rms = data.get("rms", 0)
                try:
                    async with AsyncSessionLocal() as db:
                        result = await sensor_service.process_reading(db, asset_id, rms)
                        await ws_manager.broadcast_to_asset(asset_id, result.model_dump(mode="json"))
                    logger.info(f"Modbus → Asset {asset_id} RMS={rms}")
                except Exception as e:
                    logger.error(f"Error procesando lectura Modbus asset {asset_id}: {e}")

            await asyncio.sleep(interval)

    async def start_tcp(self, host: str = None, port: int = 502):
        host = host or settings.MODBUS_HOST
        if not host:
            logger.warning("Host Modbus no configurado, lector desactivado")
            return

        self.running = True
        self.client  = AsyncModbusTcpClient(host=host, port=port)
        await self.client.connect()
        logger.info(f"Modbus TCP conectado a {host}:{port}")
        await self.poll_loop()

    async def start_rtu(self, port: str = None, baudrate: int = 9600):
        port = port or settings.SERIAL_PORT
        if not port:
            logger.warning("Puerto Modbus RTU no configurado, lector desactivado")
            return

        self.running = True
        self.client  = AsyncModbusSerialClient(port=port, baudrate=baudrate)
        await self.client.connect()
        logger.info(f"Modbus RTU conectado en {port}")
        await self.poll_loop()

    def stop(self):
        self.running = False
        if self.client:
            self.client.close()

modbus_reader = ModbusReader()