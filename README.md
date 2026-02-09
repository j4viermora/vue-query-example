# Sistema de Reservas

Aplicación full-stack para gestión de reservas con backend FastAPI y frontend Vite.

## Estructura del Proyecto

```
.
├── backend/          # API FastAPI (Python)
├── frontend/         # Aplicación Frontend (Vite + TypeScript)
└── start-dev.sh      # Script para iniciar ambos servicios
```

## Requisitos

- Python 3.13+
- Node.js y npm

## Inicio Rápido

### Opción 1: Iniciar todo con un comando

```bash
./start-dev.sh
```

### Opción 2: Iniciar servicios por separado

**Backend:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## URLs de Desarrollo

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## Backend - API de Reservas

API RESTful implementada con FastAPI siguiendo el estándar [JSON:API](https://jsonapi.org/).

### Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Información de la API |
| GET | `/health` | Health check |
| GET | `/reservas` | Listar todas las reservas |
| POST | `/reservas` | Crear una reserva |
| GET | `/reservas/{id}` | Obtener una reserva |
| PATCH | `/reservas/{id}` | Actualizar una reserva |
| DELETE | `/reservas/{id}` | Eliminar una reserva |

### Ejemplo de Uso

```bash
# Crear reserva
curl -X POST http://localhost:8000/reservas \
  -H "Content-Type: application/json" \
  -d '{"fecha": "2026-02-15", "nombre_amenity": "Piscina"}'

# Listar reservas
curl http://localhost:8000/reservas
```

## Frontend

Aplicación frontend construida con Vite y TypeScript.

### Scripts

- `npm run dev` - Iniciar servidor de desarrollo
- `npm run build` - Compilar para producción
- `npm run preview` - Previsualizar build de producción

## Tecnologías

- **Backend**: FastAPI, Pydantic, Uvicorn
- **Frontend**: Vite, TypeScript
- **Estándar**: JSON:API 1.1

## Documentación Adicional

- [Quick Start Backend](backend/QUICK_START.md)
- [Resumen de Implementación](backend/IMPLEMENTATION_SUMMARY.md)
