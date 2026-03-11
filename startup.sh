#!/bin/bash

PORT=${PORT:-8000}

cd backend

gunicorn -w 2 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:$PORT
echo "=========================================="
echo "🚀 Iniciando FastAPI en el puerto $PORT"
echo "📁 Archivo principal: backend/main.py"
echo "🔧 Instancia de FastAPI: app"
echo "=========================================="

# Iniciar la aplicación con Gunicorn
# IMPORTANTE: si cambias el nombre del archivo o la instancia,
# cambia "Main:app" por "archivo:instancia"

gunicorn -w 4 -k uvicorn.workers.UvicornWorker backend.main:app --bind 0.0.0.0:$PORT
