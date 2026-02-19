"""
Endpoints para gestión de la conexión e importación de activos desde servidor PCH.
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from app.integrations.pch_connection import PCHConnection, sync_pch_assets, PCHConnectionError

router = APIRouter(prefix="/pch", tags=["pch"])


# ─── Schemas ──────────────────────────────────────────────────────────────────

class PCHLoginRequest(BaseModel):
    host:     str = "pchcloud"   # pchcloud | local | demo
    username: str
    password: str


class PCHSyncRequest(BaseModel):
    host:     str = "pchcloud"
    username: str
    password: str


class PCHTestRequest(BaseModel):
    host:     str = "pchcloud"
    username: str
    password: str


# ─── Endpoints ────────────────────────────────────────────────────────────────

@router.post("/test-connection")
async def test_pch_connection(data: PCHTestRequest) -> Dict[str, Any]:
    """
    Verifica que las credenciales PCH son válidas y retorna la lista de dispositivos.
    Útil para el formulario de configuración del frontend antes de sincronizar.
    """
    conn = PCHConnection(
        host=data.host,
        username=data.username,
        password=data.password,
    )
    try:
        ok = await conn.login()
        if not ok:
            raise HTTPException(status_code=401, detail="Credenciales PCH incorrectas")

        devices = await conn.get_device_list()
        available = conn.get_available_devices()

        return {
            "success":      True,
            "host":         data.host,
            "device_count": len(devices) if devices else 0,
            "devices":      available,
        }
    except PCHConnectionError as e:
        raise HTTPException(status_code=502, detail=str(e))
    finally:
        await conn.logout()


@router.post("/sync")
async def sync_assets_from_pch(data: PCHSyncRequest) -> Dict[str, Any]:
    """
    Importa/actualiza todos los dispositivos PCH como activos en la DB local.
    
    - Crea activos que no existen (por tag = hostId.deviceId)
    - Actualiza nombre, localización y rpm_nominal de los existentes
    - No elimina activos locales que ya no estén en PCH
    """
    try:
        result = await sync_pch_assets(
            host=data.host,
            username=data.username,
            password=data.password,
        )
        return result
    except PCHConnectionError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sincronizando: {str(e)}")


@router.get("/hosts")
async def get_available_hosts():
    """Retorna los hosts PCH disponibles para el selector del frontend."""
    return {
        "hosts": [
            {"key": "pchcloud", "label": "PCH Cloud",  "url": "pchcloud.pch-engineering.dk"},
            {"key": "local",    "label": "Local",       "url": "localhost:8080"},
            {"key": "demo",     "label": "Demo",        "url": "demo.pchcloud.com"},
        ]
    }