
import { useMutation, useQueryClient } from '@tanstack/vue-query'
import type { Reserva, UpdateReservaPayload } from '@/types/reserva.types'
import { QueryKeys } from '@/api/query-keys'
import { updateReserva } from '@/api/queries'

type UpdateReservaParams = {
  url: string
  data: Omit<Reserva, '_links'>
}

export const useUpdateReservaMutation = () => {
  const queryClient = useQueryClient()

  const mutation = useMutation({
    mutationFn: ({
      url,
      data
    }: UpdateReservaParams) => {
      const payload: UpdateReservaPayload = {
        data: {
          type: 'reservas',
          id: data.id,
          attributes: data
        }
      }
      return updateReserva(url, payload)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [QueryKeys.Reservas] })
    },
  })

  return {
    ...mutation,
    updateReserva: mutation.mutateAsync 
  }
}
