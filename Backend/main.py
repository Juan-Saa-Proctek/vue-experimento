from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from app.api.endpoints import sensores 

app = FastAPI(title="Sistema de Monitoreo de Bombas")

# 1. Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Rutas de la API 
app.include_router(sensores.router, prefix="/api/v1", tags=["Sensores"])
# 3. Servir el frontend estático
if os.path.exists("/app/static"):
    static_path = "/app/static"
else:
    static_path = os.path.join(os.path.dirname(__file__), "..", "Frontend", "dist")
    
if os.path.exists(static_path):
    app.mount("/assets", StaticFiles(directory=os.path.join(static_path, "assets")), name="assets")
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        file_path = os.path.join(static_path, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(static_path, "index.html"))
else:
    @app.get("/")
    def root():
        return {
            "message": "Backend activo",
            "frontend_status": f"Carpeta no encontrada en: {static_path}."
        }