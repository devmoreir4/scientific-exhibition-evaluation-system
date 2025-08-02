<template>
  <div class="login-bg">
    <div class="login-header">
      <h1>XIII Mostra do Conhecimento</h1>
      <h2>e VI Feira de Oportunidades</h2>
      <div class="login-date">29/09 a 04/10 de 2025</div>
    </div>
    <div class="login-card">
      <h3>Entrar no sistema</h3>
      <form @submit.prevent="onLogin" autocomplete="off">
        <label for="siape_or_cpf">SIAPE ou CPF</label>
        <input v-model="siape_or_cpf" id="siape_or_cpf" required type="text" autocomplete="off" />
        <label for="password">Senha</label>
        <input v-model="password" id="password" type="password" required autocomplete="off" />
        <div class="user-type">
          <label>
            <input type="radio" value="evaluator" v-model="userType" /> Avaliador
          </label>
          <label>
            <input type="radio" value="admin" v-model="userType" /> Administrador
          </label>
        </div>
        <button :disabled="loading">Entrar</button>
        <p v-if="error" class="error">{{ error }}</p>
      </form>
    </div>
    <Footer :full-width="true" />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import Footer from '../components/Footer.vue'

const siape_or_cpf = ref('')
const password = ref('')
const userType = ref('evaluator')
const router = useRouter()
const auth = useAuthStore()

const loading = computed(() => auth.loading)
const error = computed(() => auth.error)

async function onLogin() {
  const siapeTrim = siape_or_cpf.value.trim()
  const passTrim = password.value.trim()
  const ok = await auth.login({ siape_or_cpf: siapeTrim, password: passTrim, isAdmin: userType.value === 'admin' })
  if (ok) {
    if (auth.role === 'admin') {
      router.push('/admin/dashboard')
    } else {
      router.push('/dashboard')
    }
  }
}
</script>

<style scoped>
.login-bg {
  min-height: 100vh;
  background: linear-gradient(135deg, #CFE3C6 0%, #F5F6FA 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  gap: 2rem;
}
.login-header {
  text-align: center;
}
.login-header h1 {
  color: #17635A;
  font-size: 2.2rem;
  font-weight: 900;
  margin-bottom: 0.2rem;
  letter-spacing: 2px;
}
.login-header h2 {
  color: #4CB050;
  font-size: 1.3rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  letter-spacing: 1px;
}
.login-date {
  background: #17635A;
  color: #fff;
  display: inline-block;
  padding: 0.3rem 1.2rem;
  border-radius: 20px;
  font-size: 1.1rem;
  font-weight: 600;
  margin-top: 0.5rem;
}
.login-card {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 4px 24px #17635a22;
  padding: 2.5rem 2rem 2rem 2rem;
  min-width: 320px;
  max-width: 350px;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: stretch;
}
.login-card h3 {
  color: #17635A;
  margin-bottom: 1.5rem;
  text-align: center;
  font-weight: 800;
  font-size: 1.3rem;
}
form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
label {
  color: #17635A;
  font-weight: 600;
  margin-bottom: 0.2rem;
}
input[type="text"],
input[type="password"] {
  padding: 0.6rem 0.8rem;
  border: 1.5px solid #CFE3C6;
  border-radius: 8px;
  font-size: 1rem;
  outline: none;
  transition: border 0.2s;
}
input:focus {
  border-color: #17635A;
}
.user-type {
  display: flex;
  gap: 1.5rem;
  justify-content: center;
  margin-bottom: 0.5rem;
}
button {
  background: #17635A;
  color: #fff;
  font-weight: 700;
  border: none;
  border-radius: 8px;
  padding: 0.7rem 0;
  font-size: 1.1rem;
  cursor: pointer;
  margin-top: 0.5rem;
  transition: background 0.2s;
}
button:disabled {
  background: #4CB050;
  opacity: 0.7;
  cursor: not-allowed;
}
.error {
  color: #b00020;
  margin-top: 0.5rem;
  text-align: center;
  font-weight: 600;
}
@media (max-width: 500px) {
  .login-bg {
    gap: 1.5rem;
  }
  .login-card {
    min-width: 90vw;
    padding: 1.2rem 0.5rem;
  }
  .login-header h1 {
    font-size: 1.3rem;
  }
  .login-header h2 {
    font-size: 1rem;
  }
  .login-date {
    font-size: 0.95rem;
  }
}
</style>
