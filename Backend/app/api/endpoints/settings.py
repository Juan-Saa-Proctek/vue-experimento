from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.models.asset import AssetUpdate, AssetResponse, AssetCreate
from app.services.asset_service import asset_service
from app.core.config import settings
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/settings", tags=["settings"])

# --- Umbrales ---
class ThresholdUpdate(BaseModel):
    rms_limit: float

@router.patch("/assets/{asset_id}/threshold", response_model=AssetResponse)
async def update_threshold(
    asset_id: int,
    data: ThresholdUpdate,
    db: AsyncSession = Depends(get_db)
):
    asset = await asset_service.update(db, asset_id, AssetUpdate(rms_limit=data.rms_limit))
    if not asset:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return asset

# --- Gestión de equipos ---
@router.get("/assets", response_model=List[AssetResponse])
async def list_assets(db: AsyncSession = Depends(get_db)):
    return await asset_service.get_all(db)

@router.post("/assets", response_model=AssetResponse, status_code=201)
async def create_asset(data: AssetCreate, db: AsyncSession = Depends(get_db)):
    existing = await asset_service.get_by_tag(db, data.tag)
    if existing:
        raise HTTPException(status_code=400, detail=f"Ya existe un equipo con el tag {data.tag}")
    return await asset_service.create(db, data)

@router.delete("/assets/{asset_id}", status_code=204)
async def delete_asset(asset_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await asset_service.delete(db, asset_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")

# --- Configuración de protocolos ---
class ProtocolConfig(BaseModel):
    mqtt_enabled:         bool = False
    mqtt_host:            Optional[str] = None
    mqtt_port:            int = 1883
    mqtt_user:            Optional[str] = None
    mqtt_password:        Optional[str] = None
    serial_enabled:       bool = False
    serial_port:          Optional[str] = None
    serial_baudrate:      int = 115200
    modbus_enabled:       bool = False
    modbus_host:          Optional[str] = None
    modbus_port:          int = 502
    pch_enabled:          bool = False
    pch_host:             Optional[str] = None
    pch_user:             Optional[str] = None
    pch_password:         Optional[str] = None
    pch_interval_minutes: int = 60

@router.get("/protocols")
async def get_protocols():
    return {
        "mqtt_enabled":         settings.MQTT_ENABLED,
        "mqtt_host":            settings.MQTT_HOST,
        "mqtt_port":            settings.MQTT_PORT,
        "serial_enabled":       settings.SERIAL_ENABLED,
        "serial_port":          settings.SERIAL_PORT,
        "serial_baudrate":      settings.SERIAL_BAUDRATE,
        "modbus_enabled":       settings.MODBUS_ENABLED,
        "modbus_host":          settings.MODBUS_HOST,
        "modbus_port":          settings.MODBUS_PORT,
        "pch_enabled":          settings.PCH_ENABLED,
        "pch_host":             settings.PCH_HOST,
        "pch_user":             settings.PCH_USER,
        "pch_password":         settings.PCH_PASSWORD,
        "pch_interval_minutes": settings.PCH_INTERVAL_MINUTES,
    }

@router.post("/protocols")
async def update_protocols(data: ProtocolConfig):
    env_lines = [
        f"MQTT_ENABLED={str(data.mqtt_enabled).lower()}",
        f"MQTT_HOST={data.mqtt_host or ''}",
        f"MQTT_PORT={data.mqtt_port}",
        f"MQTT_USER={data.mqtt_user or ''}",
        f"MQTT_PASSWORD={data.mqtt_password or ''}",
        f"SERIAL_ENABLED={str(data.serial_enabled).lower()}",
        f"SERIAL_PORT={data.serial_port or ''}",
        f"SERIAL_BAUDRATE={data.serial_baudrate}",
        f"MODBUS_ENABLED={str(data.modbus_enabled).lower()}",
        f"MODBUS_HOST={data.modbus_host or ''}",
        f"MODBUS_PORT={data.modbus_port}",
        f"PCH_ENABLED={str(data.pch_enabled).lower()}",
        f"PCH_HOST={data.pch_host or 'pchcloud'}",
        f"PCH_USER={data.pch_user or ''}",
        f"PCH_PASSWORD={data.pch_password or ''}",
        f"PCH_INTERVAL_MINUTES={data.pch_interval_minutes}",
    ]
    with open(".env", "w") as f:
        f.write("\n".join(env_lines))

    # Aplicar en memoria inmediatamente — sin reiniciar
    settings.MQTT_ENABLED         = data.mqtt_enabled
    settings.MQTT_HOST            = data.mqtt_host or ''
    settings.MQTT_PORT            = data.mqtt_port
    settings.MQTT_USER            = data.mqtt_user or ''
    settings.MQTT_PASSWORD        = data.mqtt_password or ''
    settings.SERIAL_ENABLED       = data.serial_enabled
    settings.SERIAL_PORT          = data.serial_port or ''
    settings.SERIAL_BAUDRATE      = data.serial_baudrate
    settings.MODBUS_ENABLED       = data.modbus_enabled
    settings.MODBUS_HOST          = data.modbus_host or ''
    settings.MODBUS_PORT          = data.modbus_port
    settings.PCH_ENABLED          = data.pch_enabled
    settings.PCH_HOST             = data.pch_host or 'pchcloud'
    settings.PCH_USER             = data.pch_user or ''
    settings.PCH_PASSWORD         = data.pch_password or ''
    settings.PCH_INTERVAL_MINUTES = data.pch_interval_minutes

    return {"message": "Configuración guardada y aplicada."}

# --- Estado del sistema ---
@router.get("/status")
async def get_status(db: AsyncSession = Depends(get_db)):
    assets = await asset_service.get_all(db)
    return {
        "total_assets":    len(assets),
        "online_assets":   len([a for a in assets if a.status != "offline"]),
        "critical_assets": len([a for a in assets if a.status == "critical"]),
        "protocols": {
            "mqtt":   settings.MQTT_ENABLED,
            "serial": settings.SERIAL_ENABLED,
            "modbus": settings.MODBUS_ENABLED,
        }
    }