<template>
  <div class="change-password">
    <h2>Trocar Senha</h2>
    <form @submit.prevent="changePassword">
      <label for="current">Senha Atual</label>
      <input id="current" type="password" v-model="current" required />
      <label for="new">Nova Senha</label>
      <input id="new" type="password" v-model="newPass" required />
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
  max-width: 400px;
  margin-left: auto;
  margin-right: auto;
}
h2 {
  color: #17635A;
  font-size: 1.5rem;
  margin-bottom: 1.2rem;
}
form {
  display: flex;
  flex-direction: column;
  gap: 1.1rem;
}
label {
  color: #17635A;
  font-weight: 600;
  margin-bottom: 0.2rem;
}
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
button {
  background: #4CB050;
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
  background: #CFE3C6;
  color: #17635A;
  opacity: 0.7;
}
.success {
  color: #4CB050;
  margin-top: 1rem;
  font-weight: 600;
}
.error {
  color: #b00020;
  margin-top: 1rem;
  font-weight: 600;
}
</style>
