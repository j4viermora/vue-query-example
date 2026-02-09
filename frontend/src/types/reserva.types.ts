
export type Reserva = {
  id: string
  fecha: string
  nombre_amenity: string
}

export type FormData = Omit<Reserva, 'id'>

export type CreateReservaPayload = {
  data: {
    type: 'reservas'
    attributes: FormData
  }
}

export type UpdateReservaPayload = {
  data: {
    type: 'reservas'
    id: string
    attributes: Partial<FormData>
  }
}
