import random
import numpy as np
import time

def procesar_datos_vibracion():
    # Parámetros de la simulación
    fs = 1000  # Frecuencia de muestreo (1kHz)
    t = np.linspace(0, 0.1, 100) # Una ventana de 0.1 segundos
    f_eje = 30 # 30 Hz (simulando 1800 RPM)
    
    # 1. Generamos una onda senoidal pura (el eje girando)
    señal_pura = 2.0 * np.sin(2 * np.pi * f_eje * time.time() + t)
    
    # 2. Agregamos ruido aleatorio (el "piso" de vibración)
    ruido = np.random.normal(0, 0.5, len(t))
    
    señal_final = señal_pura + ruido
    
    # Calculamos el valor RMS (el que enviaremos al Front)
    rms = np.sqrt(np.mean(señal_final**2))
    
    # Determinamos estado según norma ISO 10816 (aprox)
    estado = "Normal"
    if rms > 7.1: estado = "Peligro"
    elif rms > 4.5: estado = "Alerta"
        
    return {
        "valor": round(float(rms), 2),
        "unidad": "mm/s",
        "estado": estado,
        "frecuencia_dominante": f_eje
    }