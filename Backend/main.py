from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import sensores 

app = FastAPI(title="Sistema de Monitoreo de Bombas")

# Configuración de CORS (se mantiene igual)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# INCLUIMOS LAS RUTAS MODULARES
# prefix="/api/v1" ayuda a que mañana puedas tener una v2 sin romper el front
app.include_router(sensores.router, prefix="/api/v1", tags=["Sensores"])

@app.get("/")
def root():
    return {"message": "API de Monitoreo Activa"}