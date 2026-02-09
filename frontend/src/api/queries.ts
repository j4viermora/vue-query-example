import { apiClient } from "./config"
import { transformCollection, transformResource, type LinkObject } from "@/utils/jsonapi-transformer"
import type { Reserva, CreateReservaPayload, UpdateReservaPayload } from "@/types/reserva.types"

// Tipos de retorno simplificados
type ReservaTransformada = Reserva & {
  id: string
  type: string
  _links: Record<string, LinkObject>
}

type ReservasCollection = {
  data: ReservaTransformada[]
  _links: Record<string, LinkObject>
  meta?: Record<string, any>
}

const getReservas = async (): Promise<ReservasCollection> => {
  const { data } = await apiClient.get('/reservas')
  return transformCollection<Reserva>(data)
}

const getReserva = async (id: string): Promise<ReservaTransformada> => {
  const { data } = await apiClient.get(`/reservas/${id}`)
  return transformResource<Reserva>(data)
}

const createReserva = async (url: string, payload: CreateReservaPayload): Promise<ReservaTransformada> => {
  const { data } = await apiClient.post(url, payload)
  return transformResource<Reserva>(data)
}

const updateReserva = async (url: string, payload: UpdateReservaPayload): Promise<ReservaTransformada> => {
  const { data } = await apiClient.patch(url, payload)
  return transformResource<Reserva>(data)
}

const removeReserva = async (url: string): Promise<void> => {
  await apiClient.delete(url)
}

export {
  getReservas,
  getReserva,
  createReserva,
  updateReserva,
  removeReserva
}