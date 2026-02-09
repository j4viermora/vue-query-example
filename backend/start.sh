#!/bin/bash

# Script para iniciar la API de Reservas

echo "======================================"
echo "Iniciando API de Reservas"
echo "======================================"

# Activar entorno virtual
source venv/bin/activate

# Iniciar servidor
echo "Servidor disponible en: http://localhost:8000"
echo "Documentación interactiva: http://localhost:8000/docs"
echo "Presiona Ctrl+C para detener el servidor"
echo ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
