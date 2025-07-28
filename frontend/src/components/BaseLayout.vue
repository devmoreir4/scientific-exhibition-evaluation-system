<template>
  <div class="base-layout">
    <header>
      <div class="logo-area">
        <span class="event-title">XIII Mostra do Conhecimento</span>
        <span class="event-sub">e VI Feira de Oportunidades</span>
      </div>
      <nav>
        <router-link v-if="isAdmin" to="/admin/dashboard">Dashboard Admin</router-link>
        <router-link v-if="isAdmin" to="/admin/users">Avaliadores</router-link>
        <router-link v-if="isAdmin" to="/admin/works">Trabalhos</router-link>
        <router-link v-if="isAdmin" to="/admin/sheets">Fichas Manuais</router-link>
        <router-link v-if="isEvaluator" to="/dashboard">Dashboard Avaliador</router-link>
        <router-link v-if="isEvaluator" to="/change-password">Trocar Senha</router-link>
        <button @click="logout">Sair</button>
      </nav>
    </header>
    <main>
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'
import { computed } from 'vue'

const auth = useAuthStore()
const router = useRouter()

const isAdmin = computed(() => auth.role === 'admin')
const isEvaluator = computed(() => auth.role === 'evaluator')

function logout() {
  auth.logout()
  router.push('/login')
}
</script>

<style scoped>
.base-layout {
  min-height: 100vh;
  background: linear-gradient(135deg, #CFE3C6 0%, #F5F6FA 100%);
  display: flex;
  flex-direction: column;
}
header {
  background: #17635A;
  color: #fff;
  padding: 1rem 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
}
.logo-area {
  display: flex;
  flex-direction: column;
}
.event-title {
  font-size: 1.3rem;
  font-weight: 900;
  letter-spacing: 1px;
}
.event-sub {
  font-size: 0.95rem;
  color: #CFE3C6;
  font-weight: 600;
}
nav {
  display: flex;
  gap: 1.2rem;
  align-items: center;
}
nav a {
  color: #fff;
  text-decoration: none;
  font-weight: 600;
  padding: 0.3rem 0.7rem;
  border-radius: 6px;
  transition: background 0.2s;
}
nav a.router-link-exact-active, nav a:hover {
  background: #4CB050;
  color: #fff;
}
button {
  background: #fff;
  color: #17635A;
  border: none;
  border-radius: 6px;
  padding: 0.3rem 0.9rem;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
}
button:hover {
  background: #4CB050;
  color: #fff;
}
main {
  flex: 1;
  padding: 2rem 1rem;
  max-width: 1100px;
  margin: 0 auto;
  width: 100%;
}
@media (max-width: 700px) {
  header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
    padding: 1rem 0.5rem;
  }
  main {
    padding: 1rem 0.2rem;
  }
}
</style> 