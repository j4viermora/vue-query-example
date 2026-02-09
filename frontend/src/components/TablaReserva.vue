<script setup lang="ts">
import type { Reserva } from '@/types/reserva.types'

defineProps<{
  reservas: Reserva[]
}>()

const emit = defineEmits<{
  edit: [reserva: Reserva]
  delete: [id: string]
}>()
</script>

<template>
  <div class="bg-white rounded-2xl shadow-xl shadow-slate-200/50 border border-slate-200/60 overflow-hidden">
    <!-- Table Header -->
    <div class="bg-gradient-to-r from-slate-50 to-slate-100/50 px-6 py-4 border-b border-slate-200">
      <div class="grid grid-cols-12 gap-4 font-semibold text-slate-700 text-sm uppercase tracking-wide">
        <div class="col-span-2">ID</div>
        <div class="col-span-5">Amenidad</div>
        <div class="col-span-3">Fecha</div>
        <div class="col-span-2 text-right">Acciones</div>
      </div>
    </div>

    <!-- Table Body -->
    <div class="divide-y divide-slate-100">
      <div
        v-for="reserva in reservas"
        :key="reserva.id"
        class="grid grid-cols-12 gap-4 px-6 py-4 hover:bg-blue-50/50 transition-colors duration-150 group"
      >
        <!-- ID -->
        <div class="col-span-2 flex items-center">
          <span class="text-slate-500 font-mono text-sm">#{{ reserva.id }}</span>
        </div>

        <!-- Amenidad -->
        <div class="col-span-5 flex items-center">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-lg bg-gradient-to-br from-blue-500 to-indigo-500 flex items-center justify-center text-white font-semibold shadow-lg shadow-blue-500/30">
              {{ reserva.nombre_amenity.charAt(0) }}
            </div>
            <span class="font-medium text-slate-800">{{ reserva.nombre_amenity }}</span>
          </div>
        </div>

        <!-- Fecha -->
        <div class="col-span-3 flex items-center">
          <div class="flex items-center gap-2 text-slate-600">
            <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            <span class="text-sm">{{ reserva.fecha }}</span>
          </div>
        </div>

        <!-- Acciones -->
        <div class="col-span-2 flex items-center justify-end gap-2">
          <button
            @click="emit('edit', reserva)"
            class="p-2 text-blue-600 hover:bg-blue-100 rounded-lg transition-colors duration-150"
            title="Editar"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
          </button>
          <button
            @click="emit('delete', reserva.id)"
            class="p-2 text-red-600 hover:bg-red-100 rounded-lg transition-colors duration-150"
            title="Eliminar"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="reservas.length === 0" class="py-16 text-center">
        <div class="flex flex-col items-center gap-4">
          <div class="w-16 h-16 rounded-full bg-slate-100 flex items-center justify-center">
            <svg class="w-8 h-8 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div>
            <p class="text-slate-600 font-medium">No se encontraron reservas</p>
            <p class="text-slate-400 text-sm mt-1">Intenta con otro término de búsqueda</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
