
import { useMutation, useQueryClient } from '@tanstack/vue-query'
import type { Reserva, UpdateReservaPayload } from '@/types/reserva.types'
import { QueryKeys } from '@/api/query-keys'
import { updateReserva } from '@/api/queries'

export const useUpdateReservaMutation = () => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<Omit<Reserva, 'id'>> }) => {
      const payload: UpdateReservaPayload = {
        data: {
          type: 'reservas',
          id,
          attributes: data
        }
      }
      return updateReserva(id, payload)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [QueryKeys.Reservas] })
    },
  })
}
