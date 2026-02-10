<template>
    <div class="mt-6 flex items-center justify-between text-sm text-slate-600">
        <div>
            Mostrando <span class="font-semibold text-slate-800">{{ totalReservas }}</span> de
            <span class="font-semibold text-slate-800">{{ totalPaginas }}</span> reservas
        </div>
    </div>
</template>


<script setup lang="ts">
import { computed } from 'vue';
import { useReservasQuery } from '@/composables/useReservasQuery';

const reservasQuery = useReservasQuery()

const totalReservas = computed(() => {
    return reservasQuery.data.value?.data.length || 0
})
const totalPaginas = computed(() => {
    return reservasQuery.data.value?.data.length || 0
})

</script>