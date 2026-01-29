from fastapi import APIRouter
from app.services.vibracion import procesar_datos_vibracion
from app.services.senal import generar_senal_especifica

router = APIRouter()

@router.get("/sensor")
def leer_sensor():
    datos = procesar_datos_vibracion()
    return datos

@router.get("/senal/{tipo}")
def senal(tipo : str):
    datos = generar_senal_especifica(tipo)
    return datos