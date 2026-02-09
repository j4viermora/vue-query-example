"""
Modelos Pydantic para el recurso Reserva
"""

from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, UUID4
from uuid import uuid4


class ReservaCreate(BaseModel):
    """Modelo para crear una nueva reserva (sin id)"""

    fecha: date = Field(..., description="Fecha de la reserva en formato YYYY-MM-DD")
    nombre_amenity: str = Field(
        ..., min_length=1, max_length=100, description="Nombre de la amenidad"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "fecha": "2026-02-15",
                    "nombre_amenity": "Piscina"
                }
            ]
        }
    }


class ReservaUpdate(BaseModel):
    """Modelo para actualizar una reserva (todos los campos opcionales)"""

    fecha: Optional[date] = Field(
        None, description="Nueva fecha de la reserva en formato YYYY-MM-DD"
    )
    nombre_amenity: Optional[str] = Field(
        None, min_length=1, max_length=100, description="Nuevo nombre de la amenidad"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "nombre_amenity": "Piscina Olímpica"
                }
            ]
        }
    }


class Reserva(BaseModel):
    """Modelo completo de reserva con id"""

    id: str = Field(default_factory=lambda: str(uuid4()), description="ID único de la reserva (UUID)")
    fecha: date = Field(..., description="Fecha de la reserva")
    nombre_amenity: str = Field(..., description="Nombre de la amenidad")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "fecha": "2026-02-15",
                    "nombre_amenity": "Piscina"
                }
            ]
        }
    }
