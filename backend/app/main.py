"""
Aplicación principal FastAPI
"""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import reservas
from app.schemas.jsonapi import JsonApiErrorResponse, ErrorObject

# Crear instancia de FastAPI
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=settings.app_description,
)

# Configurar CORS
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Middleware para agregar Content-Type JSON:API a todas las respuestas
@app.middleware("http")
async def add_jsonapi_content_type(request: Request, call_next):
    """
    Middleware que agrega el Content-Type JSON:API a todas las respuestas de la API.
    Excluye endpoints de documentación para preservar su content-type original.
    """
    response = await call_next(request)

    # Excluir endpoints de documentación
    documentation_paths = ["/docs", "/redoc", "/openapi.json"]
    if request.url.path in documentation_paths:
        return response

    # Solo agregar el header si la respuesta tiene contenido
    # 204 No Content no debe tener Content-Type
    if response.status_code != status.HTTP_204_NO_CONTENT:
        # Sobrescribir el Content-Type con JSON:API para endpoints de la API
        # FastAPI establece application/json por defecto, necesitamos sobrescribirlo
        response.headers["content-type"] = settings.jsonapi_media_type

    return response


# Exception handler para errores de validación
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handler personalizado para errores de validación en formato JSON:API
    """
    errors = []
    for error in exc.errors():
        # Construir el detalle del error
        field = " -> ".join(str(loc) for loc in error["loc"])
        detail = f"Field '{field}': {error['msg']}"

        errors.append(
            ErrorObject(
                status=str(status.HTTP_422_UNPROCESSABLE_ENTITY),
                title="Validation Error",
                detail=detail,
            )
        )

    error_response = JsonApiErrorResponse(errors=errors)

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_response.model_dump(),
        media_type=settings.jsonapi_media_type,
    )


# Incluir routers
app.include_router(reservas.router)


# Endpoint raíz
@app.get(
    "/",
    summary="Información de la API",
    description="Endpoint raíz que proporciona información básica sobre la API",
)
async def root():
    """
    GET / - Información de la API

    Retorna información básica sobre la API y sus capacidades
    """
    return JSONResponse(
        content={
            "data": {
                "type": "api-info",
                "id": "1",
                "attributes": {
                    "name": settings.app_name,
                    "version": settings.app_version,
                    "description": settings.app_description,
                    "jsonapi_version": settings.jsonapi_version,
                    "endpoints": {
                        "reservas": "/reservas",
                        "documentation": "/docs",
                        "openapi": "/openapi.json",
                    },
                },
            },
            "jsonapi": {"version": settings.jsonapi_version},
        },
        media_type=settings.jsonapi_media_type,
    )


# Health check endpoint
@app.get(
    "/health",
    summary="Health check",
    description="Endpoint para verificar que la API está funcionando correctamente",
)
async def health_check():
    """
    GET /health - Health check

    Retorna el estado de la API
    """
    return JSONResponse(
        content={
            "data": {
                "type": "health",
                "id": "1",
                "attributes": {
                    "status": "healthy",
                    "service": settings.app_name,
                    "version": settings.app_version,
                },
            },
            "jsonapi": {"version": settings.jsonapi_version},
        },
        media_type=settings.jsonapi_media_type,
    )
