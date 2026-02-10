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

API RESTful implementada con FastAPI siguiendo el estándar [JSON:API v1.1](https://jsonapi.org/).

### Características

- **JSON:API v1.1**: Requests y responses completos según especificación
- **HATEOAS Mejorado**: Links con método HTTP explícito (GET, POST, PATCH, DELETE)
- **IDs Secuenciales**: Sistema simple de IDs (1, 2, 3...) en lugar de UUIDs
- **Thread-safe**: Almacenamiento en memoria con locks para concurrencia
- **CORS**: Configurado para puerto 5173 (frontend Vite)

### Endpoints

| Método | Endpoint | Descripción | Response |
|--------|----------|-------------|----------|
| GET | `/` | Información de la API | JSON:API |
| GET | `/health` | Health check | JSON:API |
| GET | `/reservas` | Listar todas las reservas | JSON:API collection |
| POST | `/reservas` | Crear una reserva | 201 + Location header |
| GET | `/reservas/{id}` | Obtener una reserva | JSON:API resource |
| PATCH | `/reservas/{id}` | Actualizar una reserva | JSON:API resource |
| DELETE | `/reservas/{id}` | Eliminar una reserva | 204 No Content |

### Ejemplo de Uso

```bash
# Crear reserva (JSON:API format)
curl -X POST http://localhost:8000/reservas \
  -H "Content-Type: application/vnd.api+json" \
  -d '{
    "data": {
      "type": "reservas",
      "attributes": {
        "fecha": "2026-02-15",
        "nombre_amenity": "Piscina"
      }
    }
  }'

# Listar reservas (incluye HATEOAS links)
curl http://localhost:8000/reservas
```

## Frontend

Aplicación Vue 3 completa con interfaz de gestión de reservas.

### Características

- **CRUD Completo**: Create, Read, Update, Delete funcional
- **TanStack Query**: Gestión de estado del servidor con cache
- **JSON:API Transformer**: Convierte respuestas a objetos planos
- **Búsqueda en Tiempo Real**: Filtrado por amenity y fecha
- **Notificaciones**: Toasts para feedback de operaciones
- **TypeScript**: Type safety completo

### Componentes

- `Header.vue` - Encabezado con botón de crear
- `SearchInput.vue` - Barra de búsqueda con filtrado
- `TablaReserva.vue` - Tabla responsive de datos
- `ModalReserva.vue` - Modal para crear/editar

### Scripts

- `npm run dev` - Iniciar servidor de desarrollo
- `npm run build` - Compilar para producción
- `npm run preview` - Previsualizar build de producción

## Tecnologías

### Backend
- **FastAPI** 0.115.0 - Framework web
- **Pydantic** 2.9.2 - Validación de datos
- **Uvicorn** 0.32.0 - Servidor ASGI
- **python-dateutil** 2.9.0 - Manejo de fechas

### Frontend
- **Vue 3** 3.5.25 - Framework (Composition API)
- **Vite** 7.3.1 - Build tool
- **TypeScript** 5.9.3 - Type safety
- **Tailwind CSS** 4.1.18 - Styling
- **TanStack Query** 5.92.9 - Data fetching
- **Axios** 1.13.5 - HTTP client
- **Vue Toastification** 2.0.0-rc.5 - Notificaciones

### Estándar
- **JSON:API 1.1** - Formato de API completo

## Documentación Adicional

- [Quick Start Backend](backend/QUICK_START.md)
- [Resumen de Implementación](backend/IMPLEMENTATION_SUMMARY.md)
