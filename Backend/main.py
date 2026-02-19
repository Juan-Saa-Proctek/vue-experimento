from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from app.core.config import settings
from app.core.websocket import ws_manager
from app.db.database import init_db, get_db
from app.api.endpoints import assets, alarms, sensors, history
from app.api.endpoints import settings as settings_router
from app.services.sensor_service import sensor_service
from app.ingestion.mqtt_client import mqtt_client
from app.ingestion.serial_reader import serial_reader
from app.ingestion.modbus_reader import modbus_reader
import asyncio
import json

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    print(f"✅ {settings.APP_NAME} v{settings.APP_VERSION} iniciado")

    # Arranca protocolos según configuración
    tasks = []
    if settings.MQTT_ENABLED:
        tasks.append(asyncio.create_task(mqtt_client.start()))
        print("📡 MQTT activado")
    if settings.SERIAL_ENABLED:
        tasks.append(asyncio.create_task(serial_reader.start()))
        print("🔌 Serial activado")
    if settings.MODBUS_ENABLED:
        tasks.append(asyncio.create_task(modbus_reader.start_tcp()))
        print("⚙️ Modbus activado")

    yield

    # Detiene protocolos al apagar
    mqtt_client.stop()
    serial_reader.stop()
    modbus_reader.stop()
    for task in tasks:
        task.cancel()
    print("🛑 Servidor apagado")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(assets.router,          prefix="/api/v1")
app.include_router(alarms.router,          prefix="/api/v1")
app.include_router(sensors.router,         prefix="/api/v1")
app.include_router(history.router,         prefix="/api/v1")
app.include_router(settings_router.router, prefix="/api/v1")

@app.websocket("/ws/{asset_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    asset_id: int,
    db: AsyncSession = Depends(get_db)
):
    await ws_manager.connect(websocket, asset_id)
    try:
        while True:
            raw    = await websocket.receive_text()
            data   = json.loads(raw)
            rms    = data.get("rms", 0)
            result = await sensor_service.process_reading(db, asset_id, rms)
            await ws_manager.broadcast_to_asset(asset_id, result.model_dump(mode="json"))
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, asset_id)

@app.get("/")
async def root():
    return {
        "app":      settings.APP_NAME,
        "version":  settings.APP_VERSION,
        "status":   "running",
        "protocols": {
            "mqtt":   settings.MQTT_ENABLED,
            "serial": settings.SERIAL_ENABLED,
            "modbus": settings.MODBUS_ENABLED
        }
    }