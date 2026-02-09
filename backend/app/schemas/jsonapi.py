"""
Esquemas de respuesta JSON:API v1.1
"""

from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field


class JsonApiVersion(BaseModel):
    """Objeto de versión JSON:API"""

    version: str = "1.1"


class LinkObject(BaseModel):
    """
    Objeto de link extendido HATEOAS con método HTTP explícito.
    
    Permite especificar el método HTTP de forma explícita para cada operación,
    haciendo la API completamente autodescriptiva.
    Compatible con JSON:API v1.1 que permite links como strings u objetos.
    """

    href: str = Field(..., description="URL del link")
    method: str = Field(
        ..., 
        description="Método HTTP para esta operación (GET, POST, PATCH, DELETE, etc.)"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "href": "http://localhost:8000/reservas/550e8400-e29b-41d4-a716-446655440000",
                    "method": "PATCH"
                }
            ]
        }
    }


class ResourceObject(BaseModel):
    """Objeto de recurso JSON:API"""

    type: str = Field(..., description="Tipo de recurso")
    id: str = Field(..., description="ID único del recurso")
    attributes: Dict[str, Any] = Field(..., description="Atributos del recurso")
    links: Optional[Dict[str, Union[str, LinkObject]]] = Field(
        None, description="Links relacionados al recurso (HATEOAS). Puede ser string o LinkObject con meta"
    )
    relationships: Optional[Dict[str, Any]] = Field(
        None, description="Relaciones con otros recursos"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
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
            ]
        }
    }


class JsonApiResponse(BaseModel):
    """Documento de respuesta JSON:API exitoso"""

    data: Union[ResourceObject, List[ResourceObject]] = Field(
        ..., description="Recurso(s) primario(s)"
    )
    links: Optional[Dict[str, Union[str, LinkObject]]] = Field(
        None, description="Links relacionados al documento (HATEOAS). Puede ser string o LinkObject con meta"
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
            ]
        }
    }


class JsonApiCreateRequest(BaseModel):
    """Request para crear un recurso en formato JSON:API"""

    class ResourceData(BaseModel):
        """Datos del recurso a crear"""
        type: str = Field(..., description="Tipo de recurso")
        attributes: Dict[str, Any] = Field(..., description="Atributos del recurso")

    data: ResourceData = Field(..., description="Datos del recurso a crear")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "data": {
                        "type": "reservas",
                        "attributes": {
                            "fecha": "2026-02-15",
                            "nombre_amenity": "Piscina"
                        }
                    }
                }
            ]
        }
    }


class JsonApiUpdateRequest(BaseModel):
    """Request para actualizar un recurso en formato JSON:API"""

    class ResourceData(BaseModel):
        """Datos del recurso a actualizar"""
        type: str = Field(..., description="Tipo de recurso")
        id: str = Field(..., description="ID del recurso")
        attributes: Dict[str, Any] = Field(..., description="Atributos a actualizar")

    data: ResourceData = Field(..., description="Datos del recurso a actualizar")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "data": {
                        "type": "reservas",
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "attributes": {
                            "nombre_amenity": "Piscina Olímpica"
                        }
                    }
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
