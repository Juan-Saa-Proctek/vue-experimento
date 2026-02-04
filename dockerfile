# --- ETAPA 1: Construcción del Frontend ---
FROM node:24-slim AS build-frontend
WORKDIR /app/frontend
COPY Frontend/package*.json ./
RUN npm install
COPY Frontend/ ./
# Cambiamos 'dev' por 'build' para optimizar la imagen
RUN npm run build 

# --- ETAPA 2: Backend y Ejecución ---
FROM python:3.12-slim
WORKDIR /app

# Instalar dependencias del sistema para ARM
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Configurar Backend
COPY Backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código del Backend
COPY Backend/ ./Backend

# Copiar el Frontend construido de la etapa anterior
COPY --from=build-frontend /app/frontend/dist ./static

# Exponer el puerto de FastAPI
EXPOSE 8092

# Comando para ejecutar FastAPI
# Usamos --host 0.0.0.0 para que sea accesible fuera del contenedor
CMD ["uvicorn", "Backend.main:app", "--host", "0.0.0.0", "--port", "8092"]