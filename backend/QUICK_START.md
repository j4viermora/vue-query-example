# Quick Start - API de Reservas

## Inicio Rápido (3 pasos)

### 1. Instalar Dependencias

```bash
cd /home/jmora/workspace/capacitacion_frontend/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Iniciar el Servidor

```bash
./start.sh
```

O manualmente:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Probar la API

Abre tu navegador en: **http://localhost:8000/docs**

## Comandos Útiles

### Ver Documentación Interactiva
```bash
# Swagger UI
open http://localhost:8000/docs

# ReDoc
open http://localhost:8000/redoc
```

### Probar Todos los Endpoints
```bash
./test_api.sh
```

### Comandos cURL Rápidos

#### Crear una reserva
```bash
curl -X POST http://localhost:8000/reservas \
  -H "Content-Type: application/json" \
  -d '{"fecha": "2026-02-15", "nombre_amenity": "Piscina"}'
```

#### Listar todas las reservas
```bash
curl http://localhost:8000/reservas | python3 -m json.tool
```

#### Ver una reserva específica
```bash
curl http://localhost:8000/reservas/{ID} | python3 -m json.tool
```

#### Actualizar una reserva
```bash
curl -X PATCH http://localhost:8000/reservas/{ID} \
  -H "Content-Type: application/json" \
  -d '{"nombre_amenity": "Piscina Olímpica"}'
```

#### Eliminar una reserva
```bash
curl -X DELETE http://localhost:8000/reservas/{ID}
```

## URLs Importantes

- **API Base**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Estructura de Respuesta (JSON:API)

### Respuesta Exitosa
```json
{
  "data": {
    "type": "reservas",
    "id": "uuid-generado",
    "attributes": {
      "fecha": "2026-02-15",
      "nombre_amenity": "Piscina"
    }
  },
  "jsonapi": {
    "version": "1.1"
  }
}
```

### Respuesta con Error
```json
{
  "errors": [
    {
      "status": "404",
      "title": "Not Found",
      "detail": "Reserva with id 'xxx' not found"
    }
  ],
  "jsonapi": {
    "version": "1.1"
  }
}
```

## Status Codes

| Code | Significado | Cuándo |
|------|-------------|--------|
| 200 | OK | GET/PATCH exitosos |
| 201 | Created | POST exitoso |
| 204 | No Content | DELETE exitoso |
| 404 | Not Found | Recurso no existe |
| 422 | Validation Error | Datos inválidos |

## Validaciones

### Campo `fecha`
- Formato: `YYYY-MM-DD` (ISO 8601)
- Ejemplo válido: `"2026-02-15"`
- Ejemplo inválido: `"15/02/2026"`, `"2026-2-15"`

### Campo `nombre_amenity`
- Tipo: String
- Longitud: 1-100 caracteres
- Requerido: Sí

## Troubleshooting

### Puerto 8000 en uso
```bash
# Encontrar proceso usando el puerto
lsof -ti:8000

# Matar el proceso
kill -9 $(lsof -ti:8000)
```

### Dependencias no instaladas
```bash
pip install -r requirements.txt
```

### Virtual environment no activado
```bash
source venv/bin/activate
```

## Recursos Adicionales

- [README.md](./README.md) - Documentación completa
- [IMPLEMENTATION_SUMMARY.md](./IMPLEMENTATION_SUMMARY.md) - Resumen de implementación
- [JSON:API Specification](https://jsonapi.org/format/) - Estándar oficial
- [FastAPI Documentation](https://fastapi.tiangolo.com/) - Documentación de FastAPI
