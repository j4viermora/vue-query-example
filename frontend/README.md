# Frontend - Vue 3 + TanStack Query (Vue Query)

## 🚀 Tecnologías

- **Vue 3** - Framework progresivo
- **TypeScript** - Tipado estático
- **TanStack Query (Vue Query)** - Gestión de estado del servidor
- **Axios** - Cliente HTTP
- **Tailwind CSS** - Framework de estilos
- **Vite** - Build tool

## 📦 Instalación

```bash
npm install
```

## 🏃 Desarrollo

```bash
npm run dev
```

El frontend estará disponible en: http://localhost:5173

## 🔧 Configuración de Vue Query

Vue Query está configurado en `src/main.ts` con las siguientes opciones por defecto:

- **refetchOnWindowFocus**: `false` - No refrescar al cambiar de ventana
- **retry**: `1` - Reintentar 1 vez en caso de error
- **staleTime**: `5 minutos` - Los datos se consideran frescos por 5 minutos

## 📚 Estructura de Composables

### `useApi.ts`
Configura la instancia de Axios con:
- Base URL del backend: `http://localhost:8000`
- Headers por defecto
- Interceptores de errores

### `useReservas.ts` (Ejemplo)
Composable que demuestra el uso de Vue Query con:

#### Queries (Lectura)
```typescript
const { reservas } = useReservas()

// Acceder a los datos
reservas.data.value // Array de reservas
reservas.isLoading.value // Estado de carga
reservas.isError.value // Estado de error
reservas.error.value // Objeto de error
```

#### Mutations (Escritura)
```typescript
const { createReserva } = useReservas()

// Crear una reserva
createReserva.mutate({
  nombre: 'Juan Pérez',
  fecha: '2026-02-10',
  hora: '19:00',
  personas: 4
})

// Acceder al estado
createReserva.isPending.value // Está procesando
createReserva.isSuccess.value // Fue exitoso
createReserva.isError.value // Hubo un error
```

## 🎯 Patrón de Uso Recomendado

### 1. Crear un composable por entidad

```typescript
// src/composables/useTuEntidad.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/vue-query'
import { useApi } from './useApi'

export const useTuEntidad = () => {
  const { client } = useApi()
  const queryClient = useQueryClient()

  // Queries
  const entidadesQuery = useQuery({
    queryKey: ['entidades'],
    queryFn: async () => {
      const { data } = await client.get('/entidades')
      return data
    },
  })

  // Mutations
  const createMutation = useMutation({
    mutationFn: async (newData) => {
      const { data } = await client.post('/entidades', newData)
      return data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['entidades'] })
    },
  })

  return {
    entidades: entidadesQuery,
    create: createMutation,
  }
}
```

### 2. Usar en componentes

```vue
<script setup lang="ts">
import { useTuEntidad } from '@/composables/useTuEntidad'

const { entidades, create } = useTuEntidad()

const handleCreate = () => {
  create.mutate({
    // datos...
  })
}
</script>

<template>
  <div v-if="entidades.isLoading">Cargando...</div>
  <div v-else-if="entidades.isError">Error: {{ entidades.error }}</div>
  <div v-else>
    <div v-for="item in entidades.data" :key="item.id">
      {{ item.nombre }}
    </div>
  </div>
</template>
```

## 🔑 Conceptos Clave

### Query Keys
Las query keys identifican únicamente cada query:
```typescript
['reservas'] // Lista de todas las reservas
['reserva', 1] // Reserva con ID 1
['reservas', { status: 'active' }] // Reservas filtradas
```

### Invalidación de Queries
Cuando modificas datos, invalida las queries relacionadas para refrescar:
```typescript
queryClient.invalidateQueries({ queryKey: ['reservas'] })
```

### Optimistic Updates (Opcional)
Actualiza la UI antes de que el servidor responda:
```typescript
onMutate: async (newData) => {
  await queryClient.cancelQueries({ queryKey: ['reservas'] })
  const previous = queryClient.getQueryData(['reservas'])
  queryClient.setQueryData(['reservas'], (old) => [...old, newData])
  return { previous }
},
onError: (err, newData, context) => {
  queryClient.setQueryData(['reservas'], context.previous)
},
```

## 📖 Recursos

- [TanStack Query Docs](https://tanstack.com/query/latest/docs/vue/overview)
- [Vue 3 Docs](https://vuejs.org/)
- [Axios Docs](https://axios-http.com/)

