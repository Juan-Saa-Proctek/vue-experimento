"""
Integración con servidor PCH Engineering para importar activos industriales.
Adaptado de la implementación original usando httpx async.
"""
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime

import httpx

logger = logging.getLogger(__name__)

DEFAULT_HOSTS_CONFIG = {
    "pchcloud": {
        "backend":       "https://pchcloud.pch-engineering.dk/backend",
        "usermanager":   "https://pchcloud.pch-engineering.dk/usermanager",
        "devicemanager": "https://pchcloud.pch-engineering.dk/devicemanager",
    },
    "local": {
        "backend":       "http://localhost:8080/backend",
        "usermanager":   "http://localhost:8080/usermanager",
        "devicemanager": "http://localhost:8080/devicemanager",
    },
    "demo": {
        "backend":       "https://demo.pchcloud.com/backend",
        "usermanager":   "https://demo.pchcloud.com/usermanager",
        "devicemanager": "https://demo.pchcloud.com/devicemanager",
    },
}


class PCHConnectionError(Exception):
    pass


class PCHConnection:
    """
    Versión async de PCHConnection usando httpx.
    Mantiene el mismo comportamiento que la versión original con requests.
    """

    def __init__(self, host: str = "pchcloud", username: str = "", password: str = ""):
        self.hosts = DEFAULT_HOSTS_CONFIG.copy()
        self.current_host = host
        self.username = username
        self.password = password
        self.session_token: Optional[str] = None
        self.device_list: Optional[List[Dict[str, Any]]] = None
        self._client: Optional[httpx.AsyncClient] = None

    @property
    def client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            # verify=False igual que el original con requests
            self._client = httpx.AsyncClient(verify=False, timeout=15.0)
        return self._client

    def get_service_url(self, service: str) -> str:
        if self.current_host not in self.hosts:
            raise PCHConnectionError(f"Host '{self.current_host}' no configurado")
        if service not in self.hosts[self.current_host]:
            raise PCHConnectionError(f"Servicio '{service}' no encontrado")
        return self.hosts[self.current_host][service]

    def is_authenticated(self) -> bool:
        return self.session_token is not None

    async def login(self) -> bool:
        """
        Autenticación igual al original:
        POST con data form-encoded, espera status 201 y retorna token.
        """
        url = f"{self.get_service_url('usermanager')}/login"
        try:
            # Igual que el original: data= (form), no json=
            response = await self.client.post(
                url,
                data={"username": self.username, "password": self.password},
            )
            logger.info(f"PCH login → {response.status_code} {response.reason_phrase}")

            if response.status_code == 201:
                self.session_token = response.json().get("token")
                return True

            logger.warning(f"PCH login fallido: {response.text[:200]}")
            return False

        except httpx.RequestError as e:
            logger.error(f"Error conectando a PCH: {e}")
            return False

    async def logout(self):
        self.session_token = None
        if self._client and not self._client.is_closed:
            await self._client.aclose()
        self._client = None

    async def get_device_list(self) -> Optional[List[Dict[str, Any]]]:
        """
        Igual al original: GET con data={'session_token': ...}
        """
        if not self.is_authenticated():
            raise PCHConnectionError("No autenticado.")

        url = f"{self.get_service_url('backend')}/device/devices"
        try:
            # El original usa data= en un GET — httpx lo manda como form body
            response = await self.client.get(
                url,
                params={"session_token": self.session_token},
            )
            logger.info(f"PCH device_list → {response.status_code}")

            if response.status_code == 200:
                self.device_list = response.json()
                return self.device_list

            logger.warning(f"get_device_list fallido: {response.text[:200]}")
            return None

        except httpx.RequestError as e:
            logger.error(f"Error obteniendo dispositivos PCH: {e}")
            return None

    def get_available_devices(self) -> List[Dict[str, str]]:
        """Igual al original — retorna deviceHostId, deviceId, key."""
        if not self.device_list:
            return []
        return [
            {
                "deviceHostId": d.get("deviceHostId", ""),
                "deviceId":     d.get("deviceId", ""),
                "key":          f"{d.get('deviceHostId', '')}.{d.get('deviceId', '')}",
                "name":         d.get("name", d.get("deviceId", "Unknown")),
            }
            for d in self.device_list
        ]


# ─── Sincronización de activos PCH → DB local ─────────────────────────────────

from app.db.database import AsyncSessionLocal
from app.services.asset_service import asset_service
from app.models.asset import AssetCreate, AssetUpdate


def _device_to_asset(device: Dict[str, Any]) -> AssetCreate:
    """
    Convierte un dispositivo PCH al esquema AssetCreate.
    Intenta varios nombres de campo porque la API PCH puede variar.
    """
    device_id  = device.get("deviceId", "UNKNOWN")
    host_id    = device.get("deviceHostId", "")
    tag        = f"{host_id}.{device_id}" if host_id else device_id

    # Nombre: intenta 'name', 'displayName', o usa el deviceId
    name = (device.get("name")
            or device.get("displayName")
            or device_id)

    # RPM nominal: varios posibles campos
    rpm_nominal = float(
        device.get("nominalSpeed")
        or device.get("rpm")
        or device.get("nominalRpm")
        or 0
    )

    # Límite RMS
    rms_limit = float(device.get("rmsLimit") or 4.5)

    # Localización
    location = (device.get("location")
                or device.get("plant")
                or device.get("site")
                or "")

    # Tipo de activo
    asset_type = (device.get("type")
                  or device.get("assetType")
                  or device.get("deviceType")
                  or "motor")

    return AssetCreate(
        tag=tag,
        name=name,
        type=asset_type,
        location=location,
        rpm_nominal=rpm_nominal,
        rms_limit=rms_limit,
    )


async def sync_pch_assets(
    host: str,
    username: str,
    password: str,
) -> Dict[str, Any]:
    """
    Login → get_device_list → crea o actualiza activos en DB local.
    Retorna resumen: { total, created, updated, errors, synced_at }
    """
    conn = PCHConnection(host=host, username=username, password=password)

    try:
        ok = await conn.login()
        if not ok:
            raise PCHConnectionError("Login fallido — verifica usuario y contraseña")

        devices = await conn.get_device_list()
        if devices is None:
            raise PCHConnectionError("No se pudo obtener la lista de dispositivos")

        created = 0
        updated = 0
        errors  = []

        async with AsyncSessionLocal() as db:
            for device in devices:
                try:
                    asset_data = _device_to_asset(device)
                    existing   = await asset_service.get_by_tag(db, asset_data.tag)

                    if existing:
                        await asset_service.update(db, existing.id, AssetUpdate(
                            name=asset_data.name,
                            location=asset_data.location,
                            rpm_nominal=asset_data.rpm_nominal,
                            rms_limit=asset_data.rms_limit,
                        ))
                        updated += 1
                        logger.info(f"PCH sync: actualizado {asset_data.tag}")
                    else:
                        await asset_service.create(db, asset_data)
                        created += 1
                        logger.info(f"PCH sync: creado {asset_data.tag}")

                except Exception as e:
                    errors.append({"device": device.get("deviceId"), "error": str(e)})
                    logger.error(f"Error sincronizando {device.get('deviceId')}: {e}")

        return {
            "total":      len(devices),
            "created":    created,
            "updated":    updated,
            "errors":     errors,
            "synced_at":  datetime.now().isoformat(),
        }

    finally:
        await conn.logout()