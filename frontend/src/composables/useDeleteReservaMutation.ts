
import { useMutation, useQueryClient } from '@tanstack/vue-query'
import { QueryKeys } from '@/api/query-keys'
import { removeReserva } from '@/api/queries'

export const useDeleteReservaMutation = () => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (id: string) => removeReserva(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [QueryKeys.Reservas] })
    },
  })
}
