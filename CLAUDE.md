# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

> **📚 For comprehensive project documentation, see [agents.md](agents.md)**  
> This file contains a quick reference. For detailed architecture, JSON:API implementation, and development guidelines, refer to agents.md.

## Project Overview

Full-stack reservation management system ("Sistema de Reservas") with FastAPI backend and Vue 3 frontend. This is an educational project demonstrating **JSON:API v1.1 complete implementation** (requests and responses) with in-memory storage.

## Development Commands

### Starting the Development Environment

**Start both services at once:**
```bash
./start-dev.sh
```

**Start services separately:**

Backend:
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Frontend:
```bash
cd frontend
npm install  # First time only
npm run dev
```

### Backend Commands

```bash
# Create/activate virtual environment
cd backend
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run server (development with auto-reload)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run without reload
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Frontend Commands

```bash
cd frontend
npm install          # Install dependencies
npm run dev          # Start dev server
npm run build        # Build for production
npm run preview      # Preview production build
```

## URLs

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **API Docs (ReDoc)**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## Backend Architecture

### Technology Stack
- **FastAPI** 0.115.0 - Web framework
- **Pydantic** 2.9.2 - Data validation
- **Uvicorn** 0.32.0 - ASGI server
- **python-dateutil** 2.9.0 - Date handling

### Directory Structure

```
backend/app/
├── main.py              # FastAPI app setup, middleware, exception handlers
├── core/
│   └── config.py        # Application settings (Pydantic-based)
├── models/
│   └── reserva.py       # Pydantic models (Reserva, ReservaCreate, ReservaUpdate)
├── schemas/
│   └── jsonapi.py       # JSON:API response schemas (ResourceObject, ErrorObject)
├── routers/
│   └── reservas.py      # CRUD endpoints for /reservas
└── storage/
    └── memory.py        # Thread-safe in-memory storage (InMemoryStorage class)
```

### Key Architectural Patterns

**Layered Architecture:**
- **Routers** handle HTTP requests/responses and validation
- **Models** define data structures with Pydantic validation
- **Schemas** format responses according to JSON:API spec
- **Storage** abstracts data persistence (currently in-memory with threading.Lock)

**JSON:API Compliance:**
- All responses use `Content-Type: application/vnd.api+json`
- Middleware in main.py automatically sets JSON:API content-type
- Resource objects have `type`, `id`, and `attributes` structure
- Error responses follow JSON:API error object format
- POST returns 201 with Location header
- DELETE returns 204 No Content
- PATCH for partial updates

**Storage Layer:**
- `InMemoryStorage` class with thread-safe operations using `threading.Lock`
- Global `storage` instance in `storage/memory.py`
- Easy to swap for database implementation (same interface)

**Data Flow:**
1. Request → Router endpoint
2. Router validates input using Pydantic models (ReservaCreate/ReservaUpdate)
3. Router calls storage methods
4. Storage performs CRUD operations on in-memory dict
5. Router converts domain model (Reserva) to JSON:API ResourceObject
6. Router returns JsonApiResponse with proper status code

### API Endpoints

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| GET | / | API info | 200 |
| GET | /health | Health check | 200 |
| POST | /reservas | Create reserva | 201 |
| GET | /reservas | List all reservas | 200 |
| GET | /reservas/{id} | Get single reserva | 200/404 |
| PATCH | /reservas/{id} | Update reserva | 200/404 |
| DELETE | /reservas/{id} | Delete reserva | 204/404 |

### Important Backend Notes

- **Storage is non-persistent**: Data is lost when server restarts
- **IDs are auto-generated**: UUIDs created automatically in Reserva model
- **Thread-safe**: All storage operations use locks for concurrent access
- **Validation**: Pydantic models validate fecha (date) and nombre_amenity (1-100 chars)
- **Error handling**: Custom exception handler in main.py formats validation errors as JSON:API

## Frontend Architecture

### Technology Stack
- **Vue 3** 3.5.25 - Framework
- **Vite** 7.3.1 - Build tool
- **TypeScript** 5.9.3 - Type safety
- **Tailwind CSS** 4.1.18 - Styling

### Project Structure

```
frontend/
├── src/
│   ├── main.ts           # App entry point
│   ├── App.vue           # Root component
│   ├── style.css         # Global styles
│   ├── components/
│   │   └── HelloWorld.vue
│   └── assets/
│       └── vue.svg
├── vite.config.ts        # Vite configuration with Vue and Tailwind plugins
└── package.json
```

### Frontend Notes

- Vue 3 with Composition API (`<script setup>`)
- TypeScript configured with vue-tsc for type checking
- Tailwind CSS v4 integrated via Vite plugin
- Currently contains starter/boilerplate code

## Adding New Features

### Backend: Adding a New Resource

1. **Create model** in `backend/app/models/`:
   - Define `{Resource}`, `{Resource}Create`, `{Resource}Update` classes
   - Use Pydantic fields with validation

2. **Add storage methods** in `backend/app/storage/memory.py`:
   - Implement CRUD methods with lock protection
   - Follow existing pattern

3. **Create router** in `backend/app/routers/`:
   - Define endpoints with proper status codes
   - Use helper function to convert model → ResourceObject
   - Return JsonApiResponse or JsonApiErrorResponse

4. **Register router** in `backend/app/main.py`:
   ```python
   from app.routers import new_resource
   app.include_router(new_resource.router)
   ```

### Frontend: Adding Components

- Create Vue components in `src/components/`
- Use TypeScript with `<script setup lang="ts">`
- Import and use in App.vue or other components

## Configuration

### Backend Settings

Settings in `backend/app/core/config.py`:
- `app_name`, `app_version`, `app_description`
- `jsonapi_version`, `jsonapi_media_type`

Modify settings by editing the `Settings` class (Pydantic BaseModel).

### Frontend Configuration

Vite config in `frontend/vite.config.ts`:
- Vue plugin for SFC support
- Tailwind CSS plugin for styling
- Add plugins or modify build settings here

## Testing the API

Use the interactive Swagger UI at http://localhost:8000/docs or curl:

```bash
# Create reservation (JSON:API format)
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

# List all reservations
curl http://localhost:8000/reservas

# Get specific reservation
curl http://localhost:8000/reservas/{id}

# Update reservation (JSON:API format)
curl -X PATCH http://localhost:8000/reservas/{id} \
  -H "Content-Type: application/vnd.api+json" \
  -d '{
    "data": {
      "type": "reservas",
      "id": "{id}",
      "attributes": {
        "nombre_amenity": "Piscina Olímpica"
      }
    }
  }'

# Delete reservation
curl -X DELETE http://localhost:8000/reservas/{id}
```

> **Note**: Requests must follow JSON:API v1.1 format with `data`, `type`, and `attributes`.  
> See [agents.md](agents.md) for complete API documentation and examples.
