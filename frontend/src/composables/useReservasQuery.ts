
import { useQuery } from '@tanstack/vue-query'
import { QueryKeys } from '@/api/query-keys'
import { getReservas } from '@/api/queries'
import { computed } from 'vue'

export const useReservasQuery = () => {
  const query = useQuery({
    queryKey: [QueryKeys.Reservas],
    queryFn: getReservas,
  })
  const crear_reserva_url = computed(() => query.data.value?._links?.crear?.href || '')
  return {
    ...query,
    crear_reserva_url,
    reservas: computed(() => query.data.value?.data || []),
  }
}
