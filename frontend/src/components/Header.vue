<script setup lang="ts">
defineEmits<{
  create: []
}>()
</script>

<template>
  <header class="bg-white/80 backdrop-blur-lg border-b border-slate-200/60 sticky top-0 z-40">
    <div class="max-w-7xl mx-auto px-6 py-6">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
            Gestión de Reservas
          </h1>
          <p class="text-slate-600 mt-1">Administra las reservas de amenidades</p>
        </div>
        <button
          @click="$emit('create')"
          class="group relative px-6 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-xl font-semibold shadow-lg shadow-blue-500/30 hover:shadow-xl hover:shadow-blue-500/40 hover:scale-105 transition-all duration-200"
        >
          <span class="flex items-center gap-2">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            Nueva Reserva
          </span>
        </button>
      </div>
    </div>
  </header>
</template>
