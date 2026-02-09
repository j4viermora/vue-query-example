import { createApp } from 'vue'
import { VueQueryPlugin, QueryClient } from '@tanstack/vue-query'
import './style.css'
import App from './App.vue'

const FIVE_MINUTES = 5 * 60 * 1000

// Configurar Vue Query Client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: FIVE_MINUTES,
    },
  },
})

const app = createApp(App)

// Instalar Vue Query
app.use(VueQueryPlugin, {
  queryClient,
})

app.mount('#app')
