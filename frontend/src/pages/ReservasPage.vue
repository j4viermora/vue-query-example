<script setup lang="ts">
import { ref, computed } from 'vue'

// ============================================================================
// Components
// ============================================================================
import SearchInput from '@/components/SearchInput.vue'
import TablaReserva from '@/components/TablaReserva.vue'
import ModalReserva from '@/components/ModalReserva.vue'
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'

// ============================================================================
// Composables
// ============================================================================

import { useReservasQuery } from '@/composables/useReservasQuery'
import { useCreateReservaMutation } from '@/composables/useCreateReservaMutation'
import { useUpdateReservaMutation } from '@/composables/useUpdateReservaMutation'
import { useToast } from 'vue-toastification'

// ============================================================================
// Types
// ============================================================================ 
import type { Reserva } from '@/types/reserva.types'

// ============================================================================
// Composables
// ============================================================================

const toast = useToast()
const { reservas, isLoading, isError } = useReservasQuery()
const createReservaMutation = useCreateReservaMutation()
const updateReservaMutation = useUpdateReservaMutation()

// ============================================================================
// State
// ============================================================================

const searchQuery = ref('')
const isModalOpen = ref(false)
const isEditMode = ref(false)
const editingReserva = ref<Reserva | null>(null)

// Form state
const formData = ref({
  nombre_amenity: '',
  fecha: '',
  id: '',
  _links: {}
})

// ============================================================================
// Computed
// ============================================================================

const filteredReservas = computed(() => {
  if (!searchQuery.value) return reservas.value

  const query = searchQuery.value.toLowerCase()
  return reservas.value.filter(
    (reserva) =>
      reserva.nombre_amenity.toLowerCase().includes(query) ||
      reserva.fecha.includes(query)
  )
})

// ============================================================================
// Methods
// ============================================================================

const openCreateModal = () => {
  isEditMode.value = false
  editingReserva.value = null
  resetForm()
  isModalOpen.value = true
}

const openEditModal = (reserva: Reserva) => {
  isEditMode.value = true
  editingReserva.value = reserva
  formData.value = {
    nombre_amenity: reserva.nombre_amenity,
    fecha: reserva.fecha,
    id: reserva.id,
    _links: reserva._links
  }
  isModalOpen.value = true
}

const closeModal = () => {
  isModalOpen.value = false
  setTimeout(() => {
    resetForm()
    isEditMode.value = false
    editingReserva.value = null
  }, 200)
}

const resetForm = () => {
  formData.value = {
    nombre_amenity: '',
    fecha: '',
    id: '',
    _links: {}
  }
}

const handleSubmit = async () => {
  const isEditAction = isEditMode.value && editingReserva.value
  try {
    if (isEditAction) {
      await updateReservaMutation.mutateAsync({
        url: editingReserva.value?._links.actualizar.href as string,
        data: {
          nombre_amenity: formData.value.nombre_amenity,
          fecha: formData.value.fecha,
          id: formData.value.id
        }
      })
      toast.success("Actualizado exitosamente")
    } else {
      await createReservaMutation.mutateAsync(formData.value)
      toast.success("Creado exitosamente")
    }
    closeModal()
  } catch (error) {
    console.error('Error al guardar:', error)
    toast.error("Error al guardar la reserva")
  }
}

const handleDelete = async (reserva:Reserva) => {
  console.log(reserva)
  if(window.confirm('¿Está seguro de que desea eliminar la reserva?')) {
    try {
     // TODO: implementar delete
     window.alert("TODO: por implementar")
    // toast.success("Eliminado exitosamente")
    } catch (error) {
      console.error('Error al eliminar:', error)
      toast.error("Error al eliminar la reserva")
    }
  }
}
</script>

<template>
  <Head>
    <title>Reservas</title>
  </Head>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
    <Header @create="openCreateModal" />

    <main class="max-w-7xl mx-auto px-6 py-8">
      <!-- Search Bar -->
      <div class="mb-6">
        <SearchInput v-model="searchQuery" />
      </div>

      <!-- Loading/Error States -->
      <div v-if="isLoading" class="flex justify-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
      
      <div v-else-if="isError" class="py-12 text-center text-red-600 bg-red-50 rounded-xl border border-red-200">
        <p class="font-semibold">Error al cargar las reservas</p>
        <p class="text-sm mt-1">Por favor verifica tu conexión o intenta más tarde</p>
      </div>

      <!-- Data Table -->
      <TablaReserva 
        v-else
        :reservas="filteredReservas"
        @edit="openEditModal"
        @delete="handleDelete"
      />

      <!-- Stats Footer -->
      <Footer 
        :filtered-reservas="filteredReservas"
        :reservas="reservas"
      />
    </main>

    <ModalReserva
      :is-open="isModalOpen"
      :is-edit-mode="isEditMode"
      v-model:form-data="formData"
      @close="closeModal"
      @submit="handleSubmit"
    />
  </div>
</template>

<style scoped>
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}
::-webkit-scrollbar-track {
  background: #f1f5f9;
}
::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>
