<script setup lang="ts">
import { computed } from 'vue'

type FormData = {
  nombre_amenity: string
  fecha: string
}

const props = defineProps<{
  isOpen: boolean
  isEditMode: boolean
  formData: FormData
  amenities: string[]
}>()

const emit = defineEmits<{
  close: []
  submit: []
  'update:formData': [data: FormData]
}>()

const modalTitle = computed(() => {
  return props.isEditMode ? 'Editar Reserva' : 'Nueva Reserva'
})

const submitButtonText = computed(() => {
  return props.isEditMode ? 'Guardar Cambios' : 'Crear Reserva'
})

const updateField = (field: keyof FormData, value: string) => {
  emit('update:formData', {
    ...props.formData,
    [field]: value
  })
}
</script>

<template>
  <Teleport to="body">
    <Transition
      enter-active-class="transition-opacity duration-200"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition-opacity duration-200"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-if="isOpen"
        class="fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-50 flex items-center justify-center p-4"
        @click.self="emit('close')"
      >
        <Transition
          enter-active-class="transition-all duration-300"
          enter-from-class="opacity-0 scale-95"
          enter-to-class="opacity-100 scale-100"
          leave-active-class="transition-all duration-200"
          leave-from-class="opacity-100 scale-100"
          leave-to-class="opacity-0 scale-95"
        >
          <div
            v-if="isOpen"
            class="bg-white rounded-2xl shadow-2xl max-w-md w-full overflow-hidden"
          >
            <!-- Modal Header -->
            <div class="bg-gradient-to-r from-blue-600 to-indigo-600 px-6 py-5">
              <div class="flex items-center justify-between">
                <h2 class="text-xl font-bold text-white">{{ modalTitle }}</h2>
                <button
                  @click="emit('close')"
                  class="text-white/80 hover:text-white hover:bg-white/10 rounded-lg p-1.5 transition-colors duration-150"
                >
                  <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>

            <!-- Modal Body -->
            <form @submit.prevent="emit('submit')" class="p-6 space-y-5">
              <!-- Amenidad Select -->
              <div>
                <label class="block text-sm font-semibold text-slate-700 mb-2">
                  Amenidad
                </label>
                <div class="relative">
                  <select
                    :value="formData.nombre_amenity"
                    @input="updateField('nombre_amenity', ($event.target as HTMLSelectElement).value)"
                    required
                    class="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500 focus:bg-white transition-all duration-200 appearance-none cursor-pointer"
                  >
                    <option value="" disabled>Selecciona una amenidad</option>
                    <option v-for="amenity in amenities" :key="amenity" :value="amenity">
                      {{ amenity }}
                    </option>
                  </select>
                  <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
                    <svg class="w-5 h-5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                    </svg>
                  </div>
                </div>
              </div>

              <!-- Fecha Input -->
              <div>
                <label class="block text-sm font-semibold text-slate-700 mb-2">
                  Fecha de Reserva
                </label>
                <div class="relative">
                  <input
                    :value="formData.fecha"
                    @input="updateField('fecha', ($event.target as HTMLInputElement).value)"
                    type="date"
                    required
                    class="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500 focus:bg-white transition-all duration-200"
                  />
                </div>
              </div>

              <!-- Modal Actions -->
              <div class="flex gap-3 pt-4">
                <button
                  type="button"
                  @click="emit('close')"
                  class="flex-1 px-4 py-3 bg-slate-100 text-slate-700 rounded-xl font-semibold hover:bg-slate-200 transition-colors duration-150"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  class="flex-1 px-4 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-xl font-semibold shadow-lg shadow-blue-500/30 hover:shadow-xl hover:shadow-blue-500/40 hover:scale-105 transition-all duration-200"
                >
                  {{ submitButtonText }}
                </button>
              </div>
            </form>
          </div>
        </Transition>
      </div>
    </Transition>
  </Teleport>
</template>
