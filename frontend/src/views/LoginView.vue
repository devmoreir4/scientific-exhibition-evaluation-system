<template>
  <div class="login-container">
    <header class="login-header">
      <h1 class="login-title">XIII Mostra do Conhecimento</h1>
      <h2 class="login-subtitle">e VI Feira de Oportunidades</h2>
    </header>

    <main class="login-main">
      <div class="login-card">
        <h3 class="card-title">Entrar no sistema</h3>

        <form class="login-form" @submit.prevent="onLogin" autocomplete="off">
          <div class="form-field">
            <label for="siape_or_cpf" class="form-label">SIAPE ou CPF</label>
            <input
              v-model="siape_or_cpf"
              id="siape_or_cpf"
              required
              type="text"
              autocomplete="off"
              class="form-input"
            />
          </div>

          <div class="form-field">
            <label for="password" class="form-label">Senha</label>
            <input
              v-model="password"
              id="password"
              type="password"
              required
              autocomplete="off"
              class="form-input"
            />
          </div>

          <div class="form-field">
            <div class="user-type">
              <label class="radio-label">
                <input type="radio" value="evaluator" v-model="userType" class="radio-input" />
                <span class="radio-text">Avaliador</span>
              </label>
              <label class="radio-label">
                <input type="radio" value="admin" v-model="userType" class="radio-input" />
                <span class="radio-text">Administrador</span>
              </label>
            </div>
          </div>

          <div class="form-field">
            <button type="submit" :disabled="loading" class="submit-button">
              Entrar
            </button>
          </div>

          <div v-if="error" class="error-container">
            <p class="error-message">{{ error }}</p>
          </div>
        </form>
      </div>
    </main>

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
.login-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #CFE3C6 0%, #F5F6FA 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  gap: 2rem;
  padding: 1rem 1rem 0 1rem;
  box-sizing: border-box;
}

.login-header {
  text-align: center;
  max-width: 600px;
  width: 100%;
}

.login-title {
  color: #17635A;
  font-size: 2.2rem;
  font-weight: 900;
  margin-bottom: 0.2rem;
  letter-spacing: 2px;
  line-height: 1.2;
}

.login-subtitle {
  color: #4CB050;
  font-size: 1.3rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  letter-spacing: 1px;
  line-height: 1.3;
}

.login-main {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.login-card {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 4px 24px #17635a22;
  padding: 2.5rem 2rem 2rem 2rem;
  min-width: 320px;
  max-width: 400px;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: stretch;
  box-sizing: border-box;
}

.card-title {
  color: #17635A;
  margin-bottom: 1.5rem;
  text-align: center;
  font-weight: 800;
  font-size: 1.3rem;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-field {
  display: flex;
  flex-direction: column;
}

.form-label {
  color: #17635A;
  font-weight: 600;
  margin-bottom: 0.2rem;
  font-size: 0.95rem;
}

.form-input {
  padding: 0.8rem 1rem;
  border: 1.5px solid #CFE3C6;
  border-radius: 8px;
  font-size: 1rem;
  outline: none;
  transition: border 0.2s;
  width: 100%;
  box-sizing: border-box;
}

.form-input:focus {
  border-color: #17635A;
  box-shadow: 0 0 0 3px rgba(23, 99, 90, 0.1);
}

.user-type {
  display: flex;
  gap: 1.5rem;
  justify-content: center;
  margin-bottom: 0.5rem;
  flex-wrap: wrap;
  align-items: center;
}

.radio-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  font-size: 0.95rem;
  white-space: nowrap;
}

.radio-input {
  width: auto;
  margin: 0;
}

.radio-text {
  color: #17635A;
  font-weight: 600;
}

.submit-button {
  background: #17635A;
  color: #fff;
  font-weight: 700;
  border: none;
  border-radius: 8px;
  padding: 0.8rem 0;
  font-size: 1.1rem;
  cursor: pointer;
  margin-top: 0.5rem;
  transition: background 0.2s;
  width: 100%;
}

.submit-button:hover:not(:disabled) {
  background: #4CB050;
}

.submit-button:disabled {
  background: #4CB050;
  opacity: 0.7;
  cursor: not-allowed;
}

.error-container {
  margin-top: 0.5rem;
}

.error-message {
  color: #b00020;
  text-align: center;
  font-weight: 600;
  font-size: 0.9rem;
  padding: 0.5rem;
  background: rgba(176, 0, 32, 0.1);
  border-radius: 6px;
}

@media (max-width: 768px) {
  .login-container {
    gap: 1.5rem;
    padding: 1rem;
  }

  .login-title {
    font-size: 1.8rem;
  }

  .login-subtitle {
    font-size: 1.1rem;
  }

  .login-card {
    max-width: 450px;
    padding: 2rem 1.5rem;
  }

  .card-title {
    font-size: 1.2rem;
  }
}

@media (max-width: 480px) {
  .login-container {
    gap: 1rem;
    padding: 1rem 1rem 0 1rem;
    justify-content: flex-start;
    padding-top: 2rem;
    min-height: 100vh;
    box-sizing: border-box;
  }

  .login-header {
    margin-bottom: 1rem;
    padding: 0 1rem;
  }

  .login-title {
    font-size: 1.4rem;
    letter-spacing: 1px;
  }

  .login-subtitle {
    font-size: 0.95rem;
    letter-spacing: 0.5px;
  }

  .login-card {
    width: 100%;
    max-width: 350px;
    padding: 1.5rem 1rem;
    border-radius: 12px;
    margin: 0 auto;
    box-sizing: border-box;
  }

  .card-title {
    font-size: 1.1rem;
    margin-bottom: 1rem;
  }

  .login-form {
    gap: 0.8rem;
  }

  .form-input {
    padding: 0.7rem 0.8rem;
    font-size: 0.95rem;
  }

  .user-type {
    gap: 1rem;
    margin-bottom: 0.3rem;
    justify-content: center;
    align-items: center;
  }

  .radio-label {
    font-size: 0.9rem;
    white-space: nowrap;
    min-width: fit-content;
  }

  .submit-button {
    padding: 0.7rem 0;
    font-size: 1rem;
  }

  .form-label {
    font-size: 0.9rem;
  }
}

@media (max-width: 360px) {
  .login-container {
    padding: 0.5rem 0.5rem 0 0.5rem;
    min-height: 100vh;
  }

  .login-header {
    padding: 0 0.5rem;
  }

  .login-title {
    font-size: 1.2rem;
  }

  .login-subtitle {
    font-size: 0.85rem;
  }

  .login-card {
    width: 100%;
    max-width: 320px;
    padding: 1.2rem 0.8rem;
    margin: 0 auto;
    box-sizing: border-box;
  }

  .card-title {
    font-size: 1rem;
  }

  .form-input {
    padding: 0.6rem 0.7rem;
    font-size: 0.9rem;
  }

  .user-type {
    flex-direction: row;
    gap: 1rem;
    align-items: center;
    justify-content: center;
  }

  .radio-label {
    white-space: nowrap;
    min-width: fit-content;
  }

  .submit-button {
    padding: 0.6rem 0;
    font-size: 0.95rem;
  }
}

@media (max-height: 600px) and (orientation: landscape) {
  .login-container {
    gap: 1rem;
    padding: 0.5rem;
  }

  .login-title {
    font-size: 1.2rem;
    margin-bottom: 0.1rem;
  }

  .login-subtitle {
    font-size: 0.9rem;
    margin-bottom: 0.3rem;
  }

  .login-card {
    padding: 1.2rem 1rem;
  }

  .card-title {
    font-size: 1rem;
    margin-bottom: 0.8rem;
  }

  .login-form {
    gap: 0.6rem;
  }

  .form-input {
    padding: 0.5rem 0.7rem;
  }

  .submit-button {
    padding: 0.5rem 0;
  }
}
</style>
