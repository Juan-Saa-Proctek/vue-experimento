import numpy as np
from scipy import signal
import time

def generar_senal_especifica(tipo="sinusoidal"):
    # Parámetros base
    fs = 1000  # Frecuencia de muestreo (1kHz)
    t_espacio = np.linspace(0, 0.1, 100, endpoint=False) # Ventana de tiempo
    f_eje = 30  # Frecuencia de la señal (30 Hz)
    fase = 2 * np.pi * f_eje * time.time() # Fase dinámica para que la onda se mueva
    
    # Generación según el tipo
    if tipo == "sinusoidal":
        señal = 2.0 * np.sin(fase + 2 * np.pi * f_eje * t_espacio)
        
    elif tipo == "cuadrada":
        # Genera una onda que alterna entre 2 y -2
        señal = 2.0 * signal.square(fase + 2 * np.pi * f_eje * t_espacio)
        
    elif tipo == "triangular":
        # Genera una onda en forma de rampa (sawtooth con width 0.5 es triangular)
        señal = 2.0 * signal.sawtooth(fase + 2 * np.pi * f_eje * t_espacio, width=0.5)
    
    else:
        señal = np.zeros(100) # Por si envían un tipo que no existe

    # Agregamos un poco de ruido para realismo
    ruido = np.random.normal(0, 0.2, len(señal))
    señal_final = señal + ruido
    
    # Cálculo de métricas
    rms = np.sqrt(np.mean(señal_final**2))
    
    return {
        "valor": round(float(rms), 2),
        "datos_onda": señal_final.tolist(), # Enviamos la lista para graficar
        "tipo": tipo,
        "unidad": "mm/s"
    }