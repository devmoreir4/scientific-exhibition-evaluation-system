import { defineStore } from 'pinia'
import api from '../axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    role: localStorage.getItem('role') || '',
    user: null,
    loading: false,
    error: null
  }),
  actions: {
    async login({ siape_or_cpf, password, isAdmin }) {
      this.loading = true
      this.error = null
      try {
        const url = isAdmin ? '/auth/admin/token' : '/auth/token'
        const payload = isAdmin
          ? { login: siape_or_cpf, password }
          : { siape_or_cpf, password }
        const { data } = await api.post(url, payload)
        this.token = data.access_token
        this.role = data.role || (isAdmin ? 'admin' : 'evaluator')
        localStorage.setItem('token', this.token)
        localStorage.setItem('role', this.role)
        api.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
        return true
      } catch (e) {
        console.error('Erro ao fazer login:', e, e.response)
        this.error = e.response?.data?.msg || JSON.stringify(e.response?.data) || e.message || 'Erro ao fazer login.'
        return false
      } finally {
        this.loading = false
      }
    },
    logout() {
      this.token = ''
      this.role = ''
      this.user = null
      localStorage.removeItem('token')
      localStorage.removeItem('role')
      delete api.defaults.headers.common['Authorization']
    },
    checkAuth() {
      if (this.token) {
        api.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
      }
    }
  }
}) 