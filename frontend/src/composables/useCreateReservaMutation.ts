
import { useMutation, useQueryClient } from '@tanstack/vue-query'
import type { Reserva, CreateReservaPayload } from '@/types/reserva.types'
import { QueryKeys } from '@/api/query-keys'
import { createReserva } from '@/api/queries'
import { useReservasQuery } from './useReservasQuery'

export const useCreateReservaMutation = () => {
  const queryClient = useQueryClient()
  const {crear_reserva_url} = useReservasQuery()

  return useMutation({
    mutationFn: (newReserva: Omit<Reserva, 'id'>) => {
      const payload: CreateReservaPayload = {
        data: {
          type: 'reservas',
          attributes: newReserva
        }
      }
      return createReserva(crear_reserva_url.value, payload)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [QueryKeys.Reservas] })
    },
  })
}
