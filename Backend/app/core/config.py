from pydantic_settings import BaseSettings
from typing import List, Optional

class Settings(BaseSettings):
    APP_NAME:    str  = "VibMonitor API"
    APP_VERSION: str  = "1.0.0"
    DEBUG:       bool = True

    # Base de datos
    DB_PATH:      str = "vibmonitor.db"
    DATABASE_URL: str = "sqlite+aiosqlite:///vibmonitor.db"

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:5173","http://127.0.0.1:5173","http://localhost:3000","http://127.0.0.1:3000"]

    # MQTT (opcional)
    MQTT_ENABLED:  bool = False
    MQTT_HOST:     str  = "localhost"
    MQTT_PORT:     int  = 1883
    MQTT_USER:     Optional[str] = None
    MQTT_PASSWORD: Optional[str] = None

    # Serial (opcional)
    SERIAL_ENABLED:  bool = False
    SERIAL_PORT:     Optional[str] = None  # ej: /dev/ttyUSB0 o COM3
    SERIAL_BAUDRATE: int  = 115200

    # Modbus (opcional)
    MODBUS_ENABLED: bool = False
    MODBUS_HOST:    Optional[str] = None  # TCP
    MODBUS_PORT:    int  = 502
    #Servidor PCH (opcional)
    PCH_ENABLED:          bool = False
    PCH_HOST:             str  = "pchcloud"
    PCH_USER:             str  = ""
    PCH_PASSWORD:         str  = ""
    PCH_INTERVAL_MINUTES: int  = 60

    class Config:
        env_file = ".env"

settings = Settings()