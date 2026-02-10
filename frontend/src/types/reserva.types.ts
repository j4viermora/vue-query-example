import type { LinkObject } from '@/utils/jsonapi-transformer'


type ReservaLinks = {
  actualizar: LinkObject
  eliminar: LinkObject
  obtener: LinkObject
}

export type Reserva = {
  id: string
  fecha: string
  nombre_amenity: string
  _links: ReservaLinks
}

export type FormData = Omit<Reserva, 'id' | '_links'>

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
