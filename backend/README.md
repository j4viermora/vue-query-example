# API de Reservas - FastAPI + JSON:API

API REST para gestión de reservas de amenidades siguiendo el estándar JSON:API v1.1.

## Características

- ✅ CRUD completo para el recurso "reservas"
- ✅ Cumplimiento total con JSON:API v1.1
- ✅ **Links HATEOAS nombrados** con métodos HTTP explícitos
- ✅ API completamente autodescriptiva
- ✅ Almacenamiento en memoria thread-safe
- ✅ Validación automática con Pydantic
- ✅ Documentación interactiva automática
- ✅ Arquitectura modular y escalable

## Estructura del Proyecto

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # Aplicación FastAPI principal
│   ├── models/
│   │   ├── __init__.py
│   │   └── reserva.py       # Modelos Pydantic
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── jsonapi.py       # Esquemas JSON:API
│   ├── routers/
│   │   ├── __init__.py
│   │   └── reservas.py      # Endpoints CRUD
│   ├── storage/
│   │   ├── __init__.py
│   │   └── memory.py        # Almacenamiento en memoria
│   └── core/
│       ├── __init__.py
│       └── config.py        # Configuración
├── requirements.txt
├── .gitignore
└── README.md
```

## Instalación

### Requisitos Previos

- Python 3.8 o superior
- pip

### Pasos de Instalación

1. **Crear y activar entorno virtual:**

```bash
python3 -m venv venv
source venv/bin/activate  # En Linux/Mac
# venv\Scripts\activate   # En Windows
```

2. **Instalar dependencias:**

```bash
pip install -r requirements.txt
```

## Ejecución

### Iniciar el servidor

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

El servidor estará disponible en: http://localhost:8000

### Documentación Interactiva

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## API Endpoints

Todos los endpoints siguen el estándar JSON:API v1.1.

### Base URL

```
http://localhost:8000
```

### Content-Type

Todas las respuestas usan:
```
Content-Type: application/vnd.api+json
```

### Endpoints Disponibles

| Método | Endpoint | Descripción | Status Code |
|--------|----------|-------------|-------------|
| GET | / | Información de la API | 200 |
| GET | /health | Health check | 200 |
| POST | /reservas | Crear reserva | 201 |
| GET | /reservas | Listar todas las reservas | 200 |
| GET | /reservas/{id} | Obtener una reserva | 200 / 404 |
| PATCH | /reservas/{id} | Actualizar reserva | 200 / 404 |
| DELETE | /reservas/{id} | Eliminar reserva | 204 / 404 |

## Ejemplos de Uso

### 1. Crear una Reserva

**Request:**
```bash
curl -X POST http://localhost:8000/reservas \
  -H "Content-Type: application/json" \
  -d '{
    "fecha": "2026-02-15",
    "nombre_amenity": "Piscina"
  }'
```

**Response (201 Created):**
```json
{
  "data": {
    "type": "reservas",
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "attributes": {
      "fecha": "2026-02-15",
      "nombre_amenity": "Piscina"
    },
    "links": {
      "reservas.obtener": {
        "href": "http://localhost:8000/reservas/550e8400-e29b-41d4-a716-446655440000",
        "method": "GET"
      },
      "reservas.actualizar": {
        "href": "http://localhost:8000/reservas/550e8400-e29b-41d4-a716-446655440000",
        "method": "PATCH"
      },
      "reservas.eliminar": {
        "href": "http://localhost:8000/reservas/550e8400-e29b-41d4-a716-446655440000",
        "method": "DELETE"
      }
    }
  },
  "jsonapi": {
    "version": "1.1"
  }
}
```

**Headers:**
```
Location: http://localhost:8000/reservas/550e8400-e29b-41d4-a716-446655440000
Content-Type: application/vnd.api+json
```

### 2. Listar Todas las Reservas

**Request:**
```bash
curl http://localhost:8000/reservas
```

**Response (200 OK):**
```json
{
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
  "data": [
    {
      "type": "reservas",
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "attributes": {
        "fecha": "2026-02-15",
        "nombre_amenity": "Piscina"
      },
      "links": {
        "reservas.obtener": {
          "href": "http://localhost:8000/reservas/550e8400-e29b-41d4-a716-446655440000",
          "method": "GET"
        },
        "reservas.actualizar": {
          "href": "http://localhost:8000/reservas/550e8400-e29b-41d4-a716-446655440000",
          "method": "PATCH"
        },
        "reservas.eliminar": {
          "href": "http://localhost:8000/reservas/550e8400-e29b-41d4-a716-446655440000",
          "method": "DELETE"
        }
      }
    }
  ],
  "jsonapi": {
    "version": "1.1"
  }
}
```

### 3. Obtener una Reserva Específica

**Request:**
```bash
curl http://localhost:8000/reservas/550e8400-e29b-41d4-a716-446655440000
```

**Response (200 OK):**
```json
{
  "data": {
    "type": "reservas",
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "attributes": {
      "fecha": "2026-02-15",
      "nombre_amenity": "Piscina"
    },
    "links": {
      "reservas.obtener": {
        "href": "http://localhost:8000/reservas/550e8400-e29b-41d4-a716-446655440000",
        "method": "GET"
      },
      "reservas.actualizar": {
        "href": "http://localhost:8000/reservas/550e8400-e29b-41d4-a716-446655440000",
        "method": "PATCH"
      },
      "reservas.eliminar": {
        "href": "http://localhost:8000/reservas/550e8400-e29b-41d4-a716-446655440000",
        "method": "DELETE"
      }
    }
  },
  "jsonapi": {
    "version": "1.1"
  }
}
```

**Error Response (404 Not Found):**
```json
{
  "errors": [
    {
      "status": "404",
      "title": "Not Found",
      "detail": "Reserva with id 'invalid-id' not found"
    }
  ],
  "jsonapi": {
    "version": "1.1"
  }
}
```

### 4. Actualizar una Reserva

**Request:**
```bash
curl -X PATCH http://localhost:8000/reservas/550e8400-e29b-41d4-a716-446655440000 \
  -H "Content-Type: application/json" \
  -d '{
    "nombre_amenity": "Piscina Olímpica"
  }'
```

**Response (200 OK):**
```json
{
  "data": {
    "type": "reservas",
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "attributes": {
      "fecha": "2026-02-15",
      "nombre_amenity": "Piscina Olímpica"
    },
    "links": {
      "reservas.obtener": {
        "href": "http://localhost:8000/reservas/550e8400-e29b-41d4-a716-446655440000",
        "method": "GET"
      },
      "reservas.actualizar": {
        "href": "http://localhost:8000/reservas/550e8400-e29b-41d4-a716-446655440000",
        "method": "PATCH"
      },
      "reservas.eliminar": {
        "href": "http://localhost:8000/reservas/550e8400-e29b-41d4-a716-446655440000",
        "method": "DELETE"
      }
    }
  },
  "jsonapi": {
    "version": "1.1"
  }
}
```

### 5. Eliminar una Reserva

**Request:**
```bash
curl -X DELETE http://localhost:8000/reservas/550e8400-e29b-41d4-a716-446655440000
```

**Response (204 No Content):**
```
(Sin contenido)
```

## Modelo de Datos

### Reserva

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| id | string (UUID) | Auto-generado | Identificador único |
| fecha | date (YYYY-MM-DD) | Sí | Fecha de la reserva |
| nombre_amenity | string (1-100) | Sí | Nombre de la amenidad |

### Validaciones

- **fecha**: Debe ser una fecha válida en formato ISO (YYYY-MM-DD)
- **nombre_amenity**: Longitud entre 1 y 100 caracteres
- **id**: Se genera automáticamente como UUID v4

## Estándar JSON:API

Esta API cumple con JSON:API v1.1. Características principales:

### Estructura de Documento Exitoso

```json
{
  "data": {
    "type": "tipo-del-recurso",
    "id": "identificador-unico",
    "attributes": {
      "campo1": "valor1",
      "campo2": "valor2"
    }
  },
  "jsonapi": {
    "version": "1.1"
  }
}
```

### Estructura de Documento con Errores

```json
{
  "errors": [
    {
      "status": "código-http",
      "title": "Título del error",
      "detail": "Descripción detallada"
    }
  ],
  "jsonapi": {
    "version": "1.1"
  }
}
```

### Características Implementadas

- ✅ Media Type: `application/vnd.api+json`
- ✅ Top-level `data` o `errors` (nunca ambos)
- ✅ Resource objects con `type`, `id`, `attributes`, `links`
- ✅ **Links HATEOAS nombrados** con métodos HTTP explícitos
- ✅ **API autodescriptiva** - cliente descubre operaciones disponibles
- ✅ Status codes HTTP correctos
- ✅ Header `Location` en respuestas POST
- ✅ PATCH para actualizaciones parciales
- ✅ DELETE retorna 204 sin body
- ✅ Errores estructurados en array

## Características Técnicas

### Almacenamiento

- **Tipo**: En memoria (diccionario Python)
- **Thread-safety**: Sí (usando `threading.Lock`)
- **Persistencia**: No (los datos se pierden al reiniciar)

### Validación

- Validación automática con Pydantic
- Mensajes de error detallados en formato JSON:API
- Validación de tipos y formatos

### Arquitectura

- Patrón de capas (routers, models, schemas, storage)
- Separación de responsabilidades
- Código modular y testeable
- Fácil migración a base de datos real

## Desarrollo

### Estructura del Código

- **main.py**: Configuración de FastAPI, middleware, exception handlers
- **models/**: Modelos Pydantic para validación de datos
- **schemas/**: Esquemas de respuesta JSON:API
- **routers/**: Endpoints y lógica de negocio
- **storage/**: Capa de almacenamiento (abstracción)
- **core/**: Configuración y utilidades

### Agregar Nuevos Endpoints

1. Crear el modelo en `models/`
2. Agregar funciones de almacenamiento en `storage/`
3. Crear el router en `routers/`
4. Incluir el router en `main.py`

### Testing

Para probar los endpoints puedes usar:

1. **Documentación interactiva**: http://localhost:8000/docs
2. **curl** (ver ejemplos arriba)
3. **Postman** o herramientas similares
4. **httpie**: `http POST localhost:8000/reservas fecha=2026-02-15 nombre_amenity=Piscina`

## Notas Importantes

- Los datos se almacenan en memoria y se pierden al reiniciar el servidor
- Los IDs se generan automáticamente como UUIDs v4
- La aplicación es thread-safe y puede manejar requests concurrentes
- El almacenamiento en memoria es solo para fines educativos

## Próximos Pasos (Fuera del Alcance Actual)

- Migrar a base de datos (PostgreSQL, MySQL, etc.)
- Agregar autenticación y autorización
- Implementar paginación
- Agregar filtros y ordenamiento
- Tests unitarios y de integración
- Logging estructurado
- Métricas y monitoreo

## Recursos

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [JSON:API Specification v1.1](https://jsonapi.org/format/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Uvicorn Documentation](https://www.uvicorn.org/)

## Licencia

Este proyecto es para fines educativos.
