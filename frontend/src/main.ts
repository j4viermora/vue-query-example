import { createApp } from 'vue'
import { VueQueryPlugin, QueryClient } from '@tanstack/vue-query'
import Toast, { type PluginOptions, POSITION } from 'vue-toastification'
import 'vue-toastification/dist/index.css'

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

// Configurar Toast options
const toastOptions: PluginOptions = {
    position: POSITION.TOP_RIGHT,
    timeout: 3000,
    closeOnClick: true,
    pauseOnFocusLoss: true,
    pauseOnHover: true,
    draggable: true,
    draggablePercent: 0.6,
    showCloseButtonOnHover: false,
    hideProgressBar: false,
    closeButton: 'button',
    icon: true,
    rtl: false
}

// Instalar plugins
app.use(Toast, toastOptions)
app.use(VueQueryPlugin, {
  queryClient,
})

app.mount('#app')
