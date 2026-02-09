"""
Almacenamiento en memoria thread-safe para reservas
"""

import threading
from typing import Dict, List, Optional
from app.models.reserva import Reserva, ReservaCreate, ReservaUpdate


class InMemoryStorage:
    """Almacenamiento en memoria thread-safe usando diccionario Python"""

    def __init__(self):
        self._storage: Dict[str, Reserva] = {}
        self._lock = threading.Lock()

    def create(self, reserva_data: ReservaCreate) -> Reserva:
        """
        Crea una nueva reserva con ID auto-generado

        Args:
            reserva_data: Datos de la reserva a crear

        Returns:
            Reserva creada con ID generado
        """
        with self._lock:
            reserva = Reserva(
                fecha=reserva_data.fecha,
                nombre_amenity=reserva_data.nombre_amenity
            )
            self._storage[reserva.id] = reserva
            return reserva

    def get(self, reserva_id: str) -> Optional[Reserva]:
        """
        Obtiene una reserva por ID

        Args:
            reserva_id: ID de la reserva

        Returns:
            Reserva si existe, None si no se encuentra
        """
        with self._lock:
            return self._storage.get(reserva_id)

    def get_all(self) -> List[Reserva]:
        """
        Obtiene todas las reservas

        Returns:
            Lista de todas las reservas
        """
        with self._lock:
            return list(self._storage.values())

    def update(self, reserva_id: str, reserva_data: ReservaUpdate) -> Optional[Reserva]:
        """
        Actualiza una reserva existente (actualización parcial)

        Args:
            reserva_id: ID de la reserva a actualizar
            reserva_data: Datos a actualizar (solo los campos proporcionados)

        Returns:
            Reserva actualizada si existe, None si no se encuentra
        """
        with self._lock:
            reserva = self._storage.get(reserva_id)
            if not reserva:
                return None

            # Actualizar solo los campos proporcionados
            update_data = reserva_data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(reserva, field, value)

            return reserva

    def delete(self, reserva_id: str) -> bool:
        """
        Elimina una reserva

        Args:
            reserva_id: ID de la reserva a eliminar

        Returns:
            True si se eliminó, False si no existía
        """
        with self._lock:
            if reserva_id in self._storage:
                del self._storage[reserva_id]
                return True
            return False


# Instancia global del storage
storage = InMemoryStorage()
