"""
Esquemas de respuesta JSON:API v1.1
"""

from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field


class JsonApiVersion(BaseModel):
    """Objeto de versión JSON:API"""

    version: str = "1.1"


class ResourceObject(BaseModel):
    """Objeto de recurso JSON:API"""

    type: str = Field(..., description="Tipo de recurso")
    id: str = Field(..., description="ID único del recurso")
    attributes: Dict[str, Any] = Field(..., description="Atributos del recurso")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "type": "reservas",
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "attributes": {
                        "fecha": "2026-02-15",
                        "nombre_amenity": "Piscina"
                    }
                }
            ]
        }
    }


class JsonApiResponse(BaseModel):
    """Documento de respuesta JSON:API exitoso"""

    data: Union[ResourceObject, List[ResourceObject]] = Field(
        ..., description="Recurso(s) primario(s)"
    )
    jsonapi: JsonApiVersion = Field(
        default_factory=JsonApiVersion, description="Objeto de versión JSON:API"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "data": {
                        "type": "reservas",
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "attributes": {
                            "fecha": "2026-02-15",
                            "nombre_amenity": "Piscina"
                        }
                    },
                    "jsonapi": {"version": "1.1"}
                }
            ]
        }
    }


class ErrorObject(BaseModel):
    """Objeto de error JSON:API"""

    status: str = Field(..., description="Código de estado HTTP como string")
    title: str = Field(..., description="Resumen breve del problema")
    detail: Optional[str] = Field(None, description="Explicación específica del problema")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "status": "404",
                    "title": "Not Found",
                    "detail": "Reserva with id '123' not found"
                }
            ]
        }
    }


class JsonApiErrorResponse(BaseModel):
    """Documento de respuesta JSON:API con errores"""

    errors: List[ErrorObject] = Field(..., description="Array de objetos de error")
    jsonapi: JsonApiVersion = Field(
        default_factory=JsonApiVersion, description="Objeto de versión JSON:API"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "errors": [
                        {
                            "status": "404",
                            "title": "Not Found",
                            "detail": "Reserva with id '123' not found"
                        }
                    ],
                    "jsonapi": {"version": "1.1"}
                }
            ]
        }
    }
