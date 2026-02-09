"""
Modelos Pydantic para el recurso Reserva
"""

from datetime import date
from typing import Optional
from pydantic import BaseModel, Field


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
    """Modelo completo de reserva con id (entero secuencial como string)"""

    id: str = Field(..., description="ID único de la reserva (Entero secuencial)")
    fecha: date = Field(..., description="Fecha de la reserva")
    nombre_amenity: str = Field(..., description="Nombre de la amenidad")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "1",
                    "fecha": "2026-02-15",
                    "nombre_amenity": "Piscina"
                }
            ]
        }
    }
