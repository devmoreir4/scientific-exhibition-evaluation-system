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
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(23, 99, 90, 0.12);
  padding: 3rem 2.5rem;
  max-width: 500px;
  margin: 2rem auto;
  width: 90%;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  min-height: 65vh;
  position: relative;
  border: 1px solid rgba(23, 99, 90, 0.08);
}

h2 {
  color: #17635A;
  font-size: 1.8rem;
  margin-bottom: 2rem;
  text-align: center;
  font-weight: 800;
  flex-shrink: 0;
  letter-spacing: 0.5px;
}

form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  flex: 1;
  justify-content: center;
}

.form-field {
  display: flex;
  flex-direction: column;
  position: relative;
}

label {
  color: #17635A;
  font-weight: 700;
  margin-bottom: 0.8rem;
  font-size: 1rem;
  letter-spacing: 0.3px;
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

input[type="password"]:focus {
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
  padding: 1rem;
  background: linear-gradient(135deg, rgba(76, 176, 80, 0.1) 0%, rgba(76, 176, 80, 0.05) 100%);
  border-radius: 12px;
  text-align: center;
  border: 1px solid rgba(76, 176, 80, 0.2);
  font-size: 0.95rem;
}

.error {
  color: #b00020;
  margin-top: 1rem;
  font-weight: 600;
  padding: 1rem;
  background: linear-gradient(135deg, rgba(176, 0, 32, 0.1) 0%, rgba(176, 0, 32, 0.05) 100%);
  border-radius: 12px;
  text-align: center;
  border: 1px solid rgba(176, 0, 32, 0.2);
  font-size: 0.95rem;
}

@media (max-width: 768px) {
  .change-password {
    padding: 2.5rem 2rem;
    margin: 1.5rem auto;
    max-width: 95%;
    min-height: 60vh;
    width: 95%;
  }

  h2 {
    font-size: 1.6rem;
    margin-bottom: 1.8rem;
  }

  form {
    gap: 1.3rem;
  }

  label {
    font-size: 0.95rem;
    margin-bottom: 0.7rem;
  }

  input[type="password"] {
    padding: 0.9rem 1.1rem;
    font-size: 0.95rem;
  }

  button {
    padding: 0.9rem 0;
    font-size: 1rem;
  }
}

@media (max-width: 480px) {
  .change-password {
    padding: 2rem 1.5rem;
    margin: 1rem auto;
    border-radius: 14px;
    min-height: 55vh;
    width: 98%;
  }

  h2 {
    font-size: 1.4rem;
    margin-bottom: 1.5rem;
  }

  form {
    gap: 1.2rem;
  }

  label {
    font-size: 0.9rem;
    margin-bottom: 0.6rem;
  }

  input[type="password"] {
    padding: 0.8rem 1rem;
    font-size: 0.9rem;
    border-radius: 10px;
  }

  button {
    padding: 0.8rem 0;
    font-size: 0.95rem;
    border-radius: 10px;
  }

  .success,
  .error {
    font-size: 0.9rem;
    padding: 0.8rem;
    border-radius: 10px;
  }
}

@media (max-width: 360px) {
  .change-password {
    padding: 1.5rem 1rem;
    margin: 0.8rem auto;
    min-height: 50vh;
    width: 99%;
  }

  h2 {
    font-size: 1.3rem;
    margin-bottom: 1.3rem;
  }

  form {
    gap: 1rem;
  }

  label {
    font-size: 0.85rem;
    margin-bottom: 0.5rem;
  }

  input[type="password"] {
    padding: 0.7rem 0.9rem;
    font-size: 0.85rem;
    border-radius: 8px;
  }

  button {
    padding: 0.7rem 0;
    font-size: 0.9rem;
    border-radius: 8px;
  }

  .success,
  .error {
    font-size: 0.85rem;
    padding: 0.7rem;
    border-radius: 8px;
  }
}

@media (max-height: 600px) and (orientation: landscape) {
  .change-password {
    margin: 1rem auto;
    min-height: 45vh;
    padding: 2rem 1.5rem;
  }

  h2 {
    font-size: 1.4rem;
    margin-bottom: 1.2rem;
  }

  form {
    gap: 1rem;
  }

  input[type="password"] {
    padding: 0.7rem 1rem;
  }

  button {
    padding: 0.7rem 0;
  }
}
</style>
