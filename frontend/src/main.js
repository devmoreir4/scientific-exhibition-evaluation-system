import { createApp } from 'vue'
import App from './App.vue'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import routes from './routes'
import { useAuthStore } from './stores/auth'

const app = createApp(App)

const pinia = createPinia()
app.use(pinia)

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const auth = useAuthStore()
  
  // Restaurar autenticação se houver token salvo
  auth.checkAuth()
  
  // Rotas públicas
  if (to.meta.public) return next()
  // Página 404
  if (to.name === 'NotFound') return next()
  // Não autenticado
  if (!auth.token) return next('/login')
  // Admin
  if (to.meta.admin && auth.role !== 'admin') return next('/dashboard')
  // Avaliador
  if (to.meta.evaluator && auth.role !== 'evaluator') return next('/admin/dashboard')
  next()
})

app.use(router)

app.mount('#app')
