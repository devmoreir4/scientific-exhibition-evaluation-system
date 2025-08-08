<template>
  <div class="change-password">
    <h2>Alterar Senha</h2>
    <form @submit.prevent="changePassword">
      <div class="form-field">
        <label for="current">Senha Atual</label>
        <input id="current" type="password" v-model="current" required />
      </div>
      <div class="form-field">
        <label for="new">Nova Senha</label>
        <input id="new" type="password" v-model="newPass" required />
      </div>
      <button type="submit" :disabled="loading">{{ loading ? 'Alterando...' : 'Alterar Senha' }}</button>
      <div v-if="successMsg" class="success">{{ successMsg }}</div>
      <div v-if="errorMsg" class="error">{{ errorMsg }}</div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../axios'

const router = useRouter()
const current = ref('')
const newPass = ref('')
const loading = ref(false)
const successMsg = ref('')
const errorMsg = ref('')

function changePassword() {
  loading.value = true
  successMsg.value = ''
  errorMsg.value = ''
  api.put('/evaluator/change-password', {
    current_password: current.value,
    new_password: newPass.value
  })
    .then(() => {
      successMsg.value = 'Senha alterada com sucesso!'
      current.value = ''
      newPass.value = ''
      setTimeout(() => {
        router.push('/dashboard')
      }, 1500)
    })
    .catch(e => { errorMsg.value = e.response?.data?.msg || 'Erro ao alterar senha.' })
    .finally(() => { loading.value = false })
}
</script>

<style scoped>
.change-password {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px #17635a22;
  padding: 2rem;
  max-width: 450px;
  margin: 1rem auto;
  width: 100%;
  box-sizing: border-box;
}

h2 {
  color: #17635A;
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
  text-align: center;
  font-weight: 700;
}

form {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

.form-field {
  display: flex;
  flex-direction: column;
}

label {
  color: #17635A;
  font-weight: 600;
  margin-bottom: 0.5rem;
  font-size: 0.95rem;
}

input[type="password"] {
  padding: 0.8rem 1rem;
  border: 1.5px solid #CFE3C6;
  border-radius: 8px;
  font-size: 1rem;
  outline: none;
  transition: border 0.2s;
  width: 100%;
  box-sizing: border-box;
}

input:focus {
  border-color: #17635A;
  box-shadow: 0 0 0 3px rgba(23, 99, 90, 0.1);
}

button {
  background: #4CB050;
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

button:hover:not(:disabled) {
  background: #17635A;
}

button:disabled {
  background: #CFE3C6;
  color: #17635A;
  opacity: 0.7;
  cursor: not-allowed;
}

.success {
  color: #4CB050;
  margin-top: 1rem;
  font-weight: 600;
  padding: 0.8rem;
  background: rgba(76, 176, 80, 0.1);
  border-radius: 6px;
  text-align: center;
}

.error {
  color: #b00020;
  margin-top: 1rem;
  font-weight: 600;
  padding: 0.8rem;
  background: rgba(176, 0, 32, 0.1);
  border-radius: 6px;
  text-align: center;
}

@media (max-width: 768px) {
  .change-password {
    padding: 1.5rem;
    margin: 0.5rem auto;
    max-width: 95%;
  }

  h2 {
    font-size: 1.3rem;
  }

  label {
    font-size: 0.9rem;
  }

  input[type="password"] {
    padding: 0.7rem 0.8rem;
    font-size: 0.95rem;
  }

  button {
    padding: 0.7rem 0;
    font-size: 1rem;
  }
}

@media (max-width: 480px) {
  .change-password {
    padding: 1rem;
    margin: 0.3rem auto;
    border-radius: 8px;
  }

  h2 {
    font-size: 1.2rem;
    margin-bottom: 1rem;
  }

  form {
    gap: 1rem;
  }

  label {
    font-size: 0.85rem;
    margin-bottom: 0.4rem;
  }

  input[type="password"] {
    padding: 0.6rem 0.7rem;
    font-size: 0.9rem;
  }

  button {
    padding: 0.6rem 0;
    font-size: 0.95rem;
  }

  .success,
  .error {
    font-size: 0.9rem;
    padding: 0.6rem;
  }
}

@media (max-width: 360px) {
  .change-password {
    padding: 0.8rem;
    margin: 0.2rem auto;
  }

  h2 {
    font-size: 1.1rem;
  }

  label {
    font-size: 0.8rem;
  }

  input[type="password"] {
    padding: 0.5rem 0.6rem;
    font-size: 0.85rem;
  }

  button {
    padding: 0.5rem 0;
    font-size: 0.9rem;
  }

  .success,
  .error {
    font-size: 0.85rem;
    padding: 0.5rem;
  }
}
</style>
