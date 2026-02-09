#!/bin/bash

# Script para iniciar Frontend y Backend simultáneamente
# Uso: ./start-dev.sh

echo "======================================"
echo "Iniciando Entorno de Desarrollo"
echo "======================================"
echo ""

# Función para limpiar procesos al salir
cleanup() {
    echo ""
    echo "======================================"
    echo "Deteniendo servicios..."
    echo "======================================"
    kill 0
    exit
}

# Capturar Ctrl+C para ejecutar cleanup
trap cleanup SIGINT SIGTERM

# Iniciar Backend
echo "🚀 Iniciando Backend (FastAPI)..."
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..

# Esperar un momento para que el backend inicie
sleep 2

# Iniciar Frontend
echo "🚀 Iniciando Frontend (Vite)..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "======================================"
echo "✅ Servicios iniciados correctamente"
echo "======================================"
echo ""
echo "📍 Frontend: http://localhost:5173"
echo "📍 Backend API: http://localhost:8000"
echo "📍 Documentación API: http://localhost:8000/docs"
echo ""
echo "Presiona Ctrl+C para detener ambos servicios"
echo ""

# Esperar a que ambos procesos terminen
wait
