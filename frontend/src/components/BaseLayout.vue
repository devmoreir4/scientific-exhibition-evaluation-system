<template>
  <div class="base-layout">
    <header>
      <div class="logo-area">
        <span class="event-title">XIII Mostra do Conhecimento</span>
        <span class="event-sub">e VI Feira de Oportunidades</span>
      </div>
      <nav>
        <router-link v-if="isAdmin" to="/admin/dashboard">Dashboard</router-link>
        <router-link v-if="isAdmin" to="/admin/distributions">Distribuições</router-link>
        <router-link v-if="isAdmin" to="/admin/monitoring">Monitoramento</router-link>
        <router-link v-if="isEvaluator" to="/dashboard">Dashboard</router-link>
        <router-link v-if="isEvaluator" to="/change-password">Alterar Senha</router-link>
        <button @click="logout">Sair</button>
      </nav>
    </header>
    <main>
      <router-view />
    </main>
    <Footer />
  </div>
</template>

<script setup>
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'
import { computed } from 'vue'
import Footer from './Footer.vue'

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
  position: relative;
}
header {
  background: #17635A;
  color: #fff;
  padding: 2rem 3rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  box-shadow: 0 2px 12px rgba(23, 99, 90, 0.15);
  gap: 2rem;
}
.logo-area {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}
.event-title {
  font-size: 1.4rem;
  font-weight: 900;
  letter-spacing: 1.2px;
  line-height: 1.2;
}
.event-sub {
  font-size: 1rem;
  color: #CFE3C6;
  font-weight: 600;
  letter-spacing: 0.5px;
}
nav {
  display: flex;
  gap: 2rem;
  align-items: center;
}
nav a {
  color: #fff;
  text-decoration: none;
  font-weight: 600;
  padding: 0.6rem 1.2rem;
  border-radius: 8px;
  transition: all 0.2s ease;
  font-size: 0.95rem;
  letter-spacing: 0.3px;
}
nav a.router-link-exact-active, nav a:hover {
  background: #4CB050;
  color: #fff;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(76, 176, 80, 0.3);
}
button {
  color: #fff;
  text-decoration: none;
  font-weight: 600;
  padding: 0.6rem 1.2rem;
  border-radius: 8px;
  transition: all 0.2s ease;
  font-size: 0.95rem;
  letter-spacing: 0.3px;
  background: transparent;
  border: none;
  cursor: pointer;
}

button:hover {
  background: #DC3545;
  color: #fff;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(220, 53, 69, 0.3);
}
main {
  flex: 1;
  padding: 2rem 1rem 2rem 1rem;
  max-width: 1100px;
  margin: 0 auto;
  width: 100%;
  min-height: 0;
}

@media (max-width: 700px) {
  header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1.5rem;
    padding: 1.5rem 1.5rem;
  }

  .logo-area {
    gap: 0.3rem;
  }

  .event-title {
    font-size: 1.3rem;
    letter-spacing: 1px;
  }

  .event-sub {
    font-size: 0.95rem;
  }

  nav {
    gap: 1.2rem;
    flex-wrap: wrap;
  }

  nav a {
    padding: 0.5rem 1rem;
    font-size: 0.9rem;
  }

  button {
    padding: 0.5rem 1.2rem;
    font-size: 0.9rem;
  }

  main {
    padding: 1.5rem 0.8rem;
  }
}
</style>
