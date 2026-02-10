# agents.md

Documentación completa del proyecto para agentes de IA (Claude, Cursor, etc.)

## Visión General del Proyecto

Sistema full-stack de gestión de reservas implementando JSON:API v1.1 con:
- **Backend**: FastAPI (Python) con almacenamiento en memoria
- **Frontend**: Vue 3 + TypeScript + Vite + Tailwind CSS
- **Estándar**: JSON:API v1.1 completo (requests y responses)

---

## Comandos de Desarrollo

### Inicio Rápido

```bash
# Iniciar backend y frontend simultáneamente
./start-dev.sh
```

### Backend

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm install  # Primera vez
npm run dev
```

---

## URLs de Desarrollo

| Servicio | URL |
|----------|-----|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |
| Health Check | http://localhost:8000/health |

---

## Backend - Arquitectura

### Stack Tecnológico

- **FastAPI** 0.115.0 - Framework web
- **Pydantic** 2.9.2 - Validación de datos
- **Uvicorn** 0.32.0 - Servidor ASGI
- **python-dateutil** 2.9.0 - Manejo de fechas

### Estructura de Directorios

```
backend/app/
├── main.py              # App FastAPI, middleware, exception handlers
├── core/
│   └── config.py        # Settings (Pydantic BaseSettings)
├── models/
│   └── reserva.py       # Modelos de dominio (Reserva, ReservaCreate, ReservaUpdate)
├── schemas/
│   └── jsonapi.py       # Schemas JSON:API (requests y responses)
├── routers/
│   └── reservas.py      # Endpoints CRUD para /reservas
└── storage/
    └── memory.py        # Almacenamiento en memoria thread-safe
```

### Patrón de Arquitectura

**Capas:**
1. **Routers** - Manejan HTTP requests/responses
2. **Models** - Definen estructuras de datos con validación Pydantic
3. **Schemas** - Formatean según JSON:API v1.1
4. **Storage** - Abstrae persistencia (actualmente in-memory)

**Flujo de Datos:**
```
Request → Router → Validación (Pydantic) → Storage → 
Domain Model → JSON:API Schema → Response
```

### Implementación JSON:API v1.1

#### Requests (POST/PATCH)

**POST /reservas:**
```json
{
  "data": {
    "type": "reservas",
    "attributes": {
      "fecha": "2026-02-15",
      "nombre_amenity": "Piscina"
    }
  }
}
```

**PATCH /reservas/{id}:**
```json
{
  "data": {
    "type": "reservas",
    "id": "1",
    "attributes": {
      "nombre_amenity": "Piscina Olímpica"
    }
  }
}
```

> **Note**: IDs are sequential integers (1, 2, 3...) returned as strings.

#### Responses

**Recurso Individual:**
```json
{
  "data": {
    "type": "reservas",
    "id": "1",
    "attributes": {
      "fecha": "2026-02-15",
      "nombre_amenity": "Piscina"
    },
    "links": {
      "reservas.obtener": {
        "href": "http://localhost:8000/reservas/1",
        "method": "GET"
      },
      "reservas.actualizar": {
        "href": "http://localhost:8000/reservas/1",
        "method": "PATCH"
      },
      "reservas.eliminar": {
        "href": "http://localhost:8000/reservas/1",
        "method": "DELETE"
      }
    },
    "relationships": null
  },
  "links": null,
  "jsonapi": {"version": "1.1"}
}
```

> **HATEOAS Mejorado**: Los links ahora son objetos con `href` y `method` explícito,
> usando nombres semánticos (reservas.obtener, reservas.actualizar, etc.) en lugar de "self".

**Colección:**
```json
{
  "data": [
    {
      "type": "reservas",
      "id": "1",
      "attributes": {...},
      "links": {
        "reservas.obtener": {"href": "...", "method": "GET"},
        "reservas.actualizar": {"href": "...", "method": "PATCH"},
        "reservas.eliminar": {"href": "...", "method": "DELETE"}
      },
      "relationships": null
    }
  ],
  "links": {
    "reservas.listar": {
      "href": "http://localhost:8000/reservas",
      "method": "GET"
    },
    "reservas.crear": {
      "href": "http://localhost:8000/reservas",
      "method": "POST"
    }
  },
  "jsonapi": {"version": "1.1"}
}
```

**Errores:**
```json
{
  "errors": [
    {
      "status": "404",
      "title": "Not Found",
      "detail": "Reserva with id 'xyz' not found"
    }
  ],
  "jsonapi": {"version": "1.1"}
}
```

### Endpoints de la API

| Método | Endpoint | Descripción | Status | Headers |
|--------|----------|-------------|--------|---------|
| GET | / | Info de la API | 200 | - |
| GET | /health | Health check | 200 | - |
| POST | /reservas | Crear reserva | 201 | Location |
| GET | /reservas | Listar reservas | 200 | - |
| GET | /reservas/{id} | Obtener reserva | 200/404 | - |
| PATCH | /reservas/{id} | Actualizar reserva | 200/404 | - |
| DELETE | /reservas/{id} | Eliminar reserva | 204/404 | - |

### Validaciones Implementadas

**POST:**
- ✅ Tipo de recurso debe ser "reservas" (409 Conflict si no coincide)
- ✅ Atributos deben ser válidos según ReservaCreate
- ✅ `fecha` debe ser formato YYYY-MM-DD
- ✅ `nombre_amenity` debe tener 1-100 caracteres

**PATCH:**
- ✅ Tipo de recurso debe ser "reservas" (409 Conflict)
- ✅ ID en body debe coincidir con ID en URL (409 Conflict)
- ✅ Atributos opcionales según ReservaUpdate
- ✅ Recurso debe existir (404 Not Found)

### Middleware y Configuración

**Middleware JSON:API** (`main.py`):
- Aplica `Content-Type: application/vnd.api+json` a todas las respuestas
- **Excluye** endpoints de documentación (`/docs`, `/redoc`, `/openapi.json`)
- Preserva content-type original para HTML

**Exception Handlers:**
- `RequestValidationError` → JSON:API error format (422)
- Errores personalizados en routers (404, 409)

### Storage Layer

**InMemoryStorage** (`storage/memory.py`):
- Thread-safe usando `threading.Lock`
- **IDs secuenciales**: Usa contador interno (1, 2, 3...) en lugar de UUIDs
- Métodos: `create()`, `get()`, `get_all()`, `update()`, `delete()`
- `get_all()` retorna reservas ordenadas por ID numérico
- Datos se pierden al reiniciar servidor
- Fácil de reemplazar con DB (misma interfaz)

---

## Frontend - Arquitectura

### Stack Tecnológico

- **Vue 3** 3.5.25 - Framework (Composition API)
- **Vite** 7.3.1 - Build tool
- **TypeScript** 5.9.3 - Type safety
- **Tailwind CSS** 4.1.18 - Styling
- **TanStack Query** 5.92.9 - Data fetching & state management ✅ **Implementado**
- **Axios** 1.13.5 - HTTP client ✅ **Implementado**
- **Vue Toastification** 2.0.0-rc.5 - Toast notifications ✅ **Implementado**

### Estructura de Directorios

```
frontend/src/
├── main.ts              # Entry point con TanStack Query setup
├── App.vue              # Root component con CRUD completo
├── style.css            # Global styles
├── api/
│   ├── config.ts        # Axios instance configurada
│   ├── queries.ts       # Funciones API con JSON:API
│   └── query-keys.ts    # Query keys para TanStack Query
├── components/
│   ├── Header.vue       # Encabezado con botón crear
│   ├── SearchInput.vue  # Componente de búsqueda
│   ├── TablaReserva.vue # Tabla de datos responsive
│   └── ModalReserva.vue # Modal crear/editar
├── composables/
│   ├── useReservasQuery.ts          # Query para listar
│   ├── useCreateReservaMutation.ts  # Mutation crear
│   ├── useUpdateReservaMutation.ts  # Mutation actualizar
│   └── useDeleteReservaMutation.ts  # Mutation eliminar
├── types/
│   └── reserva.types.ts # Tipos TypeScript
├── utils/
│   └── jsonapi-transformer.ts # Transformer JSON:API → plain objects
└── assets/
    └── vue.svg
```

### Arquitectura de Datos ✅ **Implementada**

**Flujo de datos:**
```
Componente → Composable → TanStack Query → Axios →
JSON:API Transformer → Backend API
```

**Capas implementadas:**
1. **Componentes** - UI completa con búsqueda, tabla, modal
2. **Composables** - 4 composables para CRUD completo
3. **Queries/Mutations** - TanStack Query configurado y funcionando
4. **Transformers** - `jsonapi-transformer.ts` convierte JSON:API a objetos planos
5. **Axios** - Cliente HTTP configurado con interceptors

### Configuración Implementada

**Axios** (`api/config.ts`):
```typescript
import axios from 'axios'

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const apiClient = axios.create({
  baseURL: BASE_URL,
})
```

**TanStack Query** (`main.ts`):
```typescript
import { VueQueryPlugin } from '@tanstack/vue-query'
app.use(VueQueryPlugin)
```

**JSON:API Transformer** (`utils/jsonapi-transformer.ts`):
- Convierte recursos JSON:API a objetos planos
- Simplifica nombres de links (reservas.obtener → obtener)
- Agrega campo `_links` con HATEOAS para uso fácil

### Estado Actual ✅

- ✅ Proyecto configurado con Vite + Vue 3 + TypeScript
- ✅ Tailwind CSS integrado
- ✅ Axios configurado
- ✅ **Queries/Mutations completamente implementadas**
- ✅ **4 Composables CRUD operativos**
- ✅ **UI completa: Header, SearchInput, TablaReserva, ModalReserva**
- ✅ **Vue Toastification para notificaciones**
- ✅ **Búsqueda/filtrado en tiempo real**
- ✅ **JSON:API transformer funcional**

---

## JSON:API Transformer

El frontend incluye un transformer que convierte respuestas JSON:API en objetos planos:

**Ubicación**: `frontend/src/utils/jsonapi-transformer.ts`

**Funcionalidad**:
1. **`transformResource()`** - Convierte un recurso individual
2. **`transformCollection()`** - Convierte colecciones

**Ejemplo de transformación**:

```typescript
// Respuesta JSON:API del backend
{
  type: "reservas",
  id: "1",
  attributes: { fecha: "2026-02-15", nombre_amenity: "Piscina" },
  links: {
    "reservas.obtener": { href: "...", method: "GET" },
    "reservas.actualizar": { href: "...", method: "PATCH" }
  }
}

// Después de transformResource()
{
  id: "1",
  type: "reservas",
  fecha: "2026-02-15",
  nombre_amenity: "Piscina",
  _links: {
    obtener: { href: "...", method: "GET" },      // Nombre simplificado
    actualizar: { href: "...", method: "PATCH" }  // Nombre simplificado
  }
}
```

**Beneficios**:
- Objetos planos más fáciles de usar en componentes
- Links simplificados (obtener, actualizar vs reservas.obtener, reservas.actualizar)
- Conserva método HTTP para uso HATEOAS
- Type-safe con TypeScript

---

## Agregar Nuevas Funcionalidades

### Backend: Agregar Nuevo Recurso

1. **Crear modelo** en `backend/app/models/{recurso}.py`:
```python
from pydantic import BaseModel, Field
from uuid import uuid4

class RecursoCreate(BaseModel):
    campo: str = Field(..., description="...")

class RecursoUpdate(BaseModel):
    campo: str | None = Field(None, description="...")

class Recurso(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    campo: str
```

2. **Agregar storage** en `backend/app/storage/memory.py`:
```python
class InMemoryStorage:
    def __init__(self):
        self.recursos: Dict[str, Recurso] = {}
        # ... métodos CRUD
```

3. **Crear router** en `backend/app/routers/{recurso}.py`:
```python
from fastapi import APIRouter
from app.schemas.jsonapi import JsonApiCreateRequest, JsonApiUpdateRequest

router = APIRouter(prefix="/recursos", tags=["Recursos"])

@router.post("", status_code=201)
async def create_recurso(request_body: JsonApiCreateRequest, request: Request):
    # Validar tipo
    if request_body.data.type != "recursos":
        return create_error_response(409, "Conflict", "...")
    
    # Crear recurso
    recurso_data = RecursoCreate(**request_body.data.attributes)
    recurso = storage.create(recurso_data)
    
    # Retornar JSON:API response
    resource = recurso_to_resource(recurso, request)
    return JsonApiResponse(data=resource)
```

4. **Registrar router** en `backend/app/main.py`:
```python
from app.routers import recursos
app.include_router(recursos.router)
```

### Frontend: Agregar Componente

1. **Crear componente** en `src/components/{Componente}.vue`:
```vue
<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps<{
  titulo: string
}>()

const emit = defineEmits<{
  click: [id: string]
}>()
</script>

<template>
  <div class="...">
    {{ titulo }}
  </div>
</template>
```

2. **Usar en App.vue**:
```vue
<script setup lang="ts">
import Componente from './components/Componente.vue'
</script>

<template>
  <Componente titulo="..." @click="handleClick" />
</template>
```

---

## Testing

### Backend - Usando curl

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

# Respuesta incluirá ID secuencial y links HATEOAS con method:
# {
#   "data": {
#     "type": "reservas",
#     "id": "1",
#     "links": {
#       "reservas.obtener": {"href": "...", "method": "GET"},
#       "reservas.actualizar": {"href": "...", "method": "PATCH"},
#       "reservas.eliminar": {"href": "...", "method": "DELETE"}
#     }
#   }
# }

# Listar reservas
curl http://localhost:8000/reservas

# Obtener reserva específica (usar ID secuencial: 1, 2, 3...)
curl http://localhost:8000/reservas/1

# Actualizar reserva (JSON:API format)
curl -X PATCH http://localhost:8000/reservas/1 \
  -H "Content-Type: application/vnd.api+json" \
  -d '{
    "data": {
      "type": "reservas",
      "id": "1",
      "attributes": {
        "nombre_amenity": "Piscina Olímpica"
      }
    }
  }'

# Eliminar reserva
curl -X DELETE http://localhost:8000/reservas/1
```

### Backend - Usando Swagger UI

1. Navegar a http://localhost:8000/docs
2. Expandir endpoint deseado
3. Click "Try it out"
4. Ingresar datos en formato JSON:API
5. Click "Execute"

---

## Notas Importantes

### Backend

- ✅ **JSON:API v1.1 completo**: Requests y responses siguen el estándar
- ✅ **HATEOAS mejorado**: Links con `href` y `method` explícito, nombres semánticos
- ✅ **IDs secuenciales**: Sistema de conteo simple (1, 2, 3...) en lugar de UUIDs
- ✅ **Validaciones robustas**: Tipo de recurso, ID matching, atributos
- ✅ **Thread-safe**: Storage usa locks para concurrencia
- ✅ **CORS configurado**: Puerto 5173 para frontend Vite
- ⚠️ **No persistente**: Datos se pierden al reiniciar
- ⚠️ **Sin autenticación**: API pública sin seguridad
- ⚠️ **Sin paginación**: Retorna todos los recursos

### Frontend

- ✅ **TypeScript**: Type safety en todo el código
- ✅ **Tailwind CSS v4**: Styling moderno
- ✅ **Integración completa con backend**: TanStack Query + Axios funcionando
- ✅ **CRUD completo**: Create, Read, Update, Delete operativos
- ✅ **JSON:API transformer**: Conversión automática de respuestas
- ✅ **Notificaciones**: Vue Toastification para feedback
- ✅ **Búsqueda en tiempo real**: Filtrado por amenity y fecha
- ⚠️ **Sin estado global persistente**: Solo TanStack Query cache (suficiente por ahora)

---

## Próximos Pasos Sugeridos

### Backend

1. **Paginación**: Implementar `page[number]` y `page[size]` con links
2. **Filtrado**: Agregar `filter[campo]=valor`
3. **Ordenamiento**: Implementar `sort=campo,-otro_campo`
4. **Sparse Fieldsets**: Permitir `fields[reservas]=fecha,nombre_amenity`
5. **Relaciones**: Cuando haya más recursos, implementar `relationships` e `included`
6. **Base de datos**: Reemplazar InMemoryStorage con PostgreSQL/SQLite
7. **Autenticación**: Agregar JWT o OAuth2

### Frontend

1. **Implementar queries**: Crear queries con TanStack Query
2. **Transformers**: Convertir JSON:API ↔ Domain models
3. **Composables**: Crear `useReservas()` para lógica de negocio
4. **Componentes UI**: Lista de reservas, formularios, etc.
5. **Routing**: Agregar Vue Router para navegación
6. **Estado global**: Pinia si es necesario

---

## Recursos Adicionales

- [Documentación JSON:API v1.1](https://jsonapi.org/format/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Vue 3 Docs](https://vuejs.org/)
- [TanStack Query](https://tanstack.com/query/latest)
- [Tailwind CSS](https://tailwindcss.com/)

---

## Convenciones de Código

### Backend (Python)

- **Naming**: `snake_case` para funciones y variables
- **Type hints**: Usar en todas las funciones
- **Docstrings**: Documentar endpoints y funciones públicas
- **Imports**: Ordenar alfabéticamente, agrupar por tipo

### Frontend (TypeScript)

- **Naming**: `camelCase` para variables, `PascalCase` para componentes
- **Composition API**: Usar `<script setup>` en todos los componentes
- **Props/Emits**: Definir tipos explícitamente
- **Imports**: Ordenar alfabéticamente

---

## Troubleshooting

### Backend no inicia

```bash
# Verificar que el venv esté activado
source backend/venv/bin/activate

# Reinstalar dependencias
pip install -r backend/requirements.txt

# Verificar puerto 8000 no esté en uso
lsof -i :8000
```

### Frontend no inicia

```bash
# Limpiar node_modules
rm -rf frontend/node_modules
npm install

# Verificar puerto 5173 no esté en uso
lsof -i :5173
```

### CORS errors

El backend ya tiene CORS configurado para desarrollo. Si hay problemas, verificar `main.py`.
