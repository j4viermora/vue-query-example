
import { useMutation, useQueryClient } from '@tanstack/vue-query'
import { QueryKeys } from '@/api/query-keys'
import { removeReserva } from '@/api/queries'

export const useDeleteReservaMutation = () => {
  const queryClient = useQueryClient()

  const mutation = useMutation({
    mutationFn: (url: string) => removeReserva(url),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [QueryKeys.Reservas] })
    },
  })

  return {
    ...mutation,
    deleteReserva: mutation.mutateAsync
  }
}
