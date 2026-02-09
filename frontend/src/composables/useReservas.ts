import { useQuery, useMutation, useQueryClient } from '@tanstack/vue-query'
import { apiClient } from '@/api/config'

interface Reserva {
  id: number
  nombre: string
  fecha: string
  hora: string
  personas: number
}

interface CreateReservaDto {
  nombre: string
  fecha: string
  hora: string
  personas: number
}

export const useReservas = () => {
  const queryClient = useQueryClient()

  // Query: Obtener todas las reservas
  const reservasQuery = useQuery({
    queryKey: ['reservas'],
    queryFn: async () => {
      const { data } = await apiClient.get<Reserva[]>('/reservas')
      return data
    },
  })

  // Query: Obtener una reserva por ID
  const useReservaById = (id: number) => {
    return useQuery({
      queryKey: ['reserva', id],
      queryFn: async () => {
        const { data } = await apiClient.get<Reserva>(`/reservas/${id}`)
        return data
      },
      enabled: !!id, // Solo ejecutar si hay un ID válido
    })
  }

  // Mutation: Crear una nueva reserva
  const createReservaMutation = useMutation({
    mutationFn: async (newReserva: CreateReservaDto) => {
      const { data } = await apiClient.post<Reserva>('/reservas', newReserva)
      return data
    },
    onSuccess: () => {
      // Invalidar y refrescar la lista de reservas
      queryClient.invalidateQueries({ queryKey: ['reservas'] })
    },
  })

  // Mutation: Actualizar una reserva
  const updateReservaMutation = useMutation({
    mutationFn: async ({ id, ...updateData }: Partial<Reserva> & { id: number }) => {
      const { data } = await apiClient.put<Reserva>(`/reservas/${id}`, updateData)
      return data
    },
    onSuccess: (_, variables) => {
      // Invalidar queries relacionadas
      queryClient.invalidateQueries({ queryKey: ['reservas'] })
      queryClient.invalidateQueries({ queryKey: ['reserva', variables.id] })
    },
  })

  // Mutation: Eliminar una reserva
  const deleteReservaMutation = useMutation({
    mutationFn: async (id: number) => {
      await apiClient.delete(`/reservas/${id}`)
      return id
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['reservas'] })
    },
  })

  return {
    // Queries
    reservas: reservasQuery,
    useReservaById,
    
    // Mutations
    createReserva: createReservaMutation,
    updateReserva: updateReservaMutation,
    deleteReserva: deleteReservaMutation,
  }
}
