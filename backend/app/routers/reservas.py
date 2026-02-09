"""
Router CRUD para el recurso Reservas
"""

from typing import List
from fastapi import APIRouter, HTTPException, status, Response, Request
from fastapi.responses import JSONResponse

from app.models.reserva import Reserva, ReservaCreate, ReservaUpdate
from app.schemas.jsonapi import (
    JsonApiResponse,
    JsonApiErrorResponse,
    JsonApiCreateRequest,
    JsonApiUpdateRequest,
    ResourceObject,
    ErrorObject,
)
from app.storage.memory import storage
from app.core.config import settings

router = APIRouter(prefix="/reservas", tags=["Reservas"])


def reserva_to_resource(reserva: Reserva, request: Request) -> ResourceObject:
    """
    Convierte un modelo Reserva a un ResourceObject JSON:API

    Args:
        reserva: Modelo de reserva
        request: Request object para construir URLs absolutas

    Returns:
        ResourceObject en formato JSON:API con links HATEOAS nombrados
        que incluyen método HTTP explícito para cada operación disponible
    """
    base_url = str(request.base_url).rstrip("/")
    resource_url = f"{base_url}/reservas/{reserva.id}"
    
    return ResourceObject(
        type="reservas",
        id=reserva.id,
        attributes={
            "fecha": reserva.fecha.isoformat(),
            "nombre_amenity": reserva.nombre_amenity,
        },
        links={
            "reservas.obtener": {
                "href": resource_url,
                "method": "GET"
            },
            "reservas.actualizar": {
                "href": resource_url,
                "method": "PATCH"
            },
            "reservas.eliminar": {
                "href": resource_url,
                "method": "DELETE"
            }
        },
    )


def create_error_response(status_code: int, title: str, detail: str) -> JSONResponse:
    """
    Crea una respuesta de error en formato JSON:API

    Args:
        status_code: Código de estado HTTP
        title: Título del error
        detail: Detalle del error

    Returns:
        JSONResponse con el error en formato JSON:API
    """
    error_response = JsonApiErrorResponse(
        errors=[
            ErrorObject(
                status=str(status_code),
                title=title,
                detail=detail,
            )
        ]
    )
    return JSONResponse(
        status_code=status_code,
        content=error_response.model_dump(),
        media_type=settings.jsonapi_media_type,
    )


@router.post(
    "",
    response_model=JsonApiResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una nueva reserva",
    description="Crea una nueva reserva con los datos proporcionados. El ID se genera automáticamente.",
)
async def create_reserva(request_body: JsonApiCreateRequest, request: Request):
    """
    POST /reservas - Crea una nueva reserva

    Request body debe seguir el formato JSON:API:
    ```json
    {
      "data": {
        "type": "reservas",
        "attributes": {
          "fecha": "YYYY-MM-DD",
          "nombre_amenity": "string"
        }
      }
    }
    ```

    Retorna la reserva creada con status 201, header Location,
    y links HATEOAS nombrados con métodos HTTP explícitos.
    """
    # Validar que el tipo de recurso sea correcto
    if request_body.data.type != "reservas":
        return create_error_response(
            status_code=status.HTTP_409_CONFLICT,
            title="Conflict",
            detail=f"Resource type must be 'reservas', got '{request_body.data.type}'",
        )
    
    # Extraer atributos y crear modelo ReservaCreate
    try:
        reserva_data = ReservaCreate(**request_body.data.attributes)
    except Exception as e:
        return create_error_response(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            title="Validation Error",
            detail=str(e),
        )
    
    reserva = storage.create(reserva_data)
    resource = reserva_to_resource(reserva, request)
    response_data = JsonApiResponse(data=resource)

    # Construir URL completa del recurso creado
    base_url = str(request.base_url).rstrip("/")
    location = f"{base_url}/reservas/{reserva.id}"

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=response_data.model_dump(),
        headers={"Location": location},
        media_type=settings.jsonapi_media_type,
    )


@router.get(
    "",
    response_model=JsonApiResponse,
    summary="Listar todas las reservas",
    description="Obtiene una lista de todas las reservas existentes.",
)
async def list_reservas(request: Request):
    """
    GET /reservas - Lista todas las reservas

    Retorna un array de reservas en formato JSON:API con links HATEOAS
    nombrados que incluyen operaciones de colección (listar, crear) y
    operaciones de recurso individual en cada item.
    """
    reservas = storage.get_all()
    resources = [reserva_to_resource(reserva, request) for reserva in reservas]
    
    base_url = str(request.base_url).rstrip("/")
    response_data = JsonApiResponse(
        data=resources,
        links={
            "reservas.listar": {
                "href": f"{base_url}/reservas",
                "method": "GET"
            },
            "reservas.crear": {
                "href": f"{base_url}/reservas",
                "method": "POST"
            }
        }
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=response_data.model_dump(),
        media_type=settings.jsonapi_media_type,
    )


@router.get(
    "/{reserva_id}",
    response_model=JsonApiResponse,
    summary="Obtener una reserva específica",
    description="Obtiene los detalles de una reserva por su ID.",
    responses={
        200: {"description": "Reserva encontrada"},
        404: {
            "description": "Reserva no encontrada",
            "model": JsonApiErrorResponse,
        },
    },
)
async def get_reserva(reserva_id: str, request: Request):
    """
    GET /reservas/{reserva_id} - Obtiene una reserva por ID

    - **reserva_id**: ID único de la reserva (UUID)

    Retorna la reserva si existe con links HATEOAS nombrados
    (reservas.obtener, reservas.actualizar, reservas.eliminar),
    error 404 si no se encuentra.
    """
    reserva = storage.get(reserva_id)

    if not reserva:
        return create_error_response(
            status_code=status.HTTP_404_NOT_FOUND,
            title="Not Found",
            detail=f"Reserva with id '{reserva_id}' not found",
        )

    resource = reserva_to_resource(reserva, request)
    response_data = JsonApiResponse(data=resource)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=response_data.model_dump(),
        media_type=settings.jsonapi_media_type,
    )


@router.patch(
    "/{reserva_id}",
    response_model=JsonApiResponse,
    summary="Actualizar una reserva",
    description="Actualiza parcialmente una reserva existente. Solo los campos proporcionados serán actualizados.",
    responses={
        200: {"description": "Reserva actualizada exitosamente"},
        404: {
            "description": "Reserva no encontrada",
            "model": JsonApiErrorResponse,
        },
    },
)
async def update_reserva(reserva_id: str, request_body: JsonApiUpdateRequest, request: Request):
    """
    PATCH /reservas/{reserva_id} - Actualiza una reserva parcialmente

    Request body debe seguir el formato JSON:API:
    ```json
    {
      "data": {
        "type": "reservas",
        "id": "{reserva_id}",
        "attributes": {
          "fecha": "YYYY-MM-DD",  // opcional
          "nombre_amenity": "string"  // opcional
        }
      }
    }
    ```

    Solo se actualizan los campos proporcionados.
    Retorna la reserva actualizada con links HATEOAS nombrados,
    o error 404 si no existe.
    """
    # Validar que el tipo de recurso sea correcto
    if request_body.data.type != "reservas":
        return create_error_response(
            status_code=status.HTTP_409_CONFLICT,
            title="Conflict",
            detail=f"Resource type must be 'reservas', got '{request_body.data.type}'",
        )
    
    # Validar que el ID del body coincida con el ID del path
    if request_body.data.id != reserva_id:
        return create_error_response(
            status_code=status.HTTP_409_CONFLICT,
            title="Conflict",
            detail=f"Resource id in body ('{request_body.data.id}') must match id in URL ('{reserva_id}')",
        )
    
    # Extraer atributos y crear modelo ReservaUpdate
    try:
        reserva_data = ReservaUpdate(**request_body.data.attributes)
    except Exception as e:
        return create_error_response(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            title="Validation Error",
            detail=str(e),
        )
    
    reserva = storage.update(reserva_id, reserva_data)

    if not reserva:
        return create_error_response(
            status_code=status.HTTP_404_NOT_FOUND,
            title="Not Found",
            detail=f"Reserva with id '{reserva_id}' not found",
        )

    resource = reserva_to_resource(reserva, request)
    response_data = JsonApiResponse(data=resource)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=response_data.model_dump(),
        media_type=settings.jsonapi_media_type,
    )


@router.delete(
    "/{reserva_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar una reserva",
    description="Elimina una reserva existente.",
    responses={
        204: {"description": "Reserva eliminada exitosamente"},
        404: {
            "description": "Reserva no encontrada",
            "model": JsonApiErrorResponse,
        },
    },
)
async def delete_reserva(reserva_id: str):
    """
    DELETE /reservas/{reserva_id} - Elimina una reserva

    - **reserva_id**: ID único de la reserva (UUID)

    Retorna 204 sin contenido si se eliminó exitosamente,
    error 404 si no existe.
    """
    deleted = storage.delete(reserva_id)

    if not deleted:
        return create_error_response(
            status_code=status.HTTP_404_NOT_FOUND,
            title="Not Found",
            detail=f"Reserva with id '{reserva_id}' not found",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
