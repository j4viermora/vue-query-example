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
    ResourceObject,
    ErrorObject,
)
from app.storage.memory import storage
from app.core.config import settings

router = APIRouter(prefix="/reservas", tags=["Reservas"])


def reserva_to_resource(reserva: Reserva) -> ResourceObject:
    """
    Convierte un modelo Reserva a un ResourceObject JSON:API

    Args:
        reserva: Modelo de reserva

    Returns:
        ResourceObject en formato JSON:API
    """
    return ResourceObject(
        type="reservas",
        id=reserva.id,
        attributes={
            "fecha": reserva.fecha.isoformat(),
            "nombre_amenity": reserva.nombre_amenity,
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
async def create_reserva(reserva_data: ReservaCreate, request: Request):
    """
    POST /reservas - Crea una nueva reserva

    - **fecha**: Fecha de la reserva en formato YYYY-MM-DD
    - **nombre_amenity**: Nombre de la amenidad (1-100 caracteres)

    Retorna la reserva creada con status 201 y header Location
    """
    reserva = storage.create(reserva_data)
    resource = reserva_to_resource(reserva)
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
async def list_reservas():
    """
    GET /reservas - Lista todas las reservas

    Retorna un array de reservas en formato JSON:API
    """
    reservas = storage.get_all()
    resources = [reserva_to_resource(reserva) for reserva in reservas]
    response_data = JsonApiResponse(data=resources)

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
async def get_reserva(reserva_id: str):
    """
    GET /reservas/{reserva_id} - Obtiene una reserva por ID

    - **reserva_id**: ID único de la reserva (UUID)

    Retorna la reserva si existe, error 404 si no se encuentra
    """
    reserva = storage.get(reserva_id)

    if not reserva:
        return create_error_response(
            status_code=status.HTTP_404_NOT_FOUND,
            title="Not Found",
            detail=f"Reserva with id '{reserva_id}' not found",
        )

    resource = reserva_to_resource(reserva)
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
async def update_reserva(reserva_id: str, reserva_data: ReservaUpdate):
    """
    PATCH /reservas/{reserva_id} - Actualiza una reserva parcialmente

    - **reserva_id**: ID único de la reserva (UUID)
    - **fecha** (opcional): Nueva fecha de la reserva
    - **nombre_amenity** (opcional): Nuevo nombre de la amenidad

    Solo se actualizan los campos proporcionados.
    Retorna la reserva actualizada o error 404 si no existe.
    """
    reserva = storage.update(reserva_id, reserva_data)

    if not reserva:
        return create_error_response(
            status_code=status.HTTP_404_NOT_FOUND,
            title="Not Found",
            detail=f"Reserva with id '{reserva_id}' not found",
        )

    resource = reserva_to_resource(reserva)
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
