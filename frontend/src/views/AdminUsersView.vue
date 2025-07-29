<template>
  <div class="admin-users">
    <h2>Avaliadores</h2>
    <button class="add-btn" @click="openModal()">Cadastrar Avaliador</button>
    <div v-if="loading" class="loading">Carregando avaliadores...</div>
    <div v-else>
      <table>
        <thead>
          <tr>
            <th>Nome</th>
            <th>SIAPE/CPF</th>
            <th>Área</th>
            <th>Subáreas</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.name }}</td>
            <td>{{ user.siape_or_cpf }}</td>
            <td>{{ user.area }}</td>
            <td>{{ user.subareas }}</td>
            <td>
              <button class="edit-btn" @click="openModal(user)">Editar</button>
              <button class="remove-btn" @click="removeUser(user.id)">Remover</button>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-if="error" class="error">{{ error }}</div>
    </div>

    <div v-if="showModal" class="modal-bg">
      <div class="modal">
        <h3>{{ editingUser ? 'Editar Avaliador' : 'Cadastrar Avaliador' }}</h3>
        <form @submit.prevent="saveUser">
          <label>Nome</label>
          <input v-model="form.name" required />
          <label>SIAPE/CPF</label>
          <input v-model="form.siape_or_cpf" required />
          <label>Área</label>
          <input v-model="form.area" required />
          <label>Subáreas</label>
          <input v-model="form.subareas" required placeholder="Separadas por ponto e vírgula (;)" />
          <label>Data de Nascimento</label>
          <input v-model="form.birthdate" required placeholder="DDMMAAAA" />
          <div class="modal-actions">
            <button type="submit">Salvar</button>
            <button type="button" @click="closeModal">Cancelar</button>
          </div>
        </form>
        <div v-if="modalError" class="error">{{ modalError }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import api from '../axios'

const users = ref([])
const loading = ref(true)
const error = ref('')
const showModal = ref(false)
const editingUser = ref(null)
const modalError = ref('')
const form = reactive({ name: '', siape_or_cpf: '', area: '', subareas: '', birthdate: '' })

function fetchUsers() {
  loading.value = true
  error.value = ''
  api.get('/admin/users')
    .then(res => { 
      console.log('Resposta /admin/users:', res)
      users.value = res.data.users 
    })
    .catch(e => { 
      console.error('Erro /admin/users:', e, e.response)
      error.value = e.response?.data?.msg || JSON.stringify(e.response?.data) || e.message || 'Erro ao buscar avaliadores.' 
    })
    .finally(() => { loading.value = false })
}

function openModal(user = null) {
  showModal.value = true
  editingUser.value = user
  if (user) {
    Object.assign(form, user)
  } else {
    Object.assign(form, { name: '', siape_or_cpf: '', area: '', subareas: '', birthdate: '' })
  }
  modalError.value = ''
}

function closeModal() {
  showModal.value = false
  editingUser.value = null
  modalError.value = ''
}

function saveUser() {
  modalError.value = ''
  const payload = { ...form }
  if (editingUser.value) {
    api.put(`/admin/users/${editingUser.value.id}`, payload)
      .then(() => { fetchUsers(); closeModal() })
      .catch(e => { modalError.value = e.response?.data?.msg || 'Erro ao editar avaliador.' })
  } else {
    api.post('/auth/register', payload)
      .then(() => { fetchUsers(); closeModal() })
      .catch(e => { modalError.value = e.response?.data?.msg || 'Erro ao cadastrar avaliador.' })
  }
}

function removeUser(id) {
  if (!confirm('Tem certeza que deseja remover este avaliador?')) return
  api.delete(`/admin/users/${id}`)
    .then(() => fetchUsers())
    .catch(e => { error.value = e.response?.data?.msg || 'Erro ao remover avaliador.' })
}

onMounted(fetchUsers)
</script>

<style scoped>
.admin-users {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px #17635a22;
  padding: 2rem;
  margin-top: 1rem;
}
h2 {
  color: #17635A;
  font-size: 1.5rem;
  margin-bottom: 1.2rem;
}
.add-btn {
  background: #4CB050;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 0.5rem 1.2rem;
  font-weight: 700;
  margin-bottom: 1.2rem;
  cursor: pointer;
  transition: background 0.2s;
}
.add-btn:hover {
  background: #17635A;
}
table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 1rem;
}
th, td {
  padding: 0.7rem 0.5rem;
  text-align: left;
}
th {
  background: #CFE3C6;
  color: #17635A;
  font-weight: 800;
}
tbody tr:nth-child(even) {
  background: #F5F6FA;
}
.edit-btn, .remove-btn {
  border: none;
  border-radius: 6px;
  padding: 0.3rem 0.8rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
  min-width: 80px;
  width: 80px;
  text-align: center;
  display: block;
}
.edit-btn {
  background: #CFE3C6;
  color: #17635A;
}
.edit-btn:hover {
  background: #4CB050;
  color: #fff;
}
.remove-btn {
  background: #fff0f0;
  color: #b00020;
}
.remove-btn:hover {
  background: #b00020;
  color: #fff;
}
.loading {
  color: #17635A;
  font-weight: 600;
  margin: 2rem 0;
}
.error {
  color: #b00020;
  margin-top: 1rem;
  font-weight: 600;
}
.modal-bg {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: #0006;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
.modal {
  background: #fff;
  border-radius: 12px;
  padding: 2rem 1.5rem;
  min-width: 320px;
  max-width: 95vw;
  box-shadow: 0 2px 16px #17635a33;
}
.modal h3 {
  color: #17635A;
  margin-bottom: 1rem;
}
.modal label {
  color: #17635A;
  font-weight: 600;
  margin-top: 0.7rem;
}
.modal input {
  width: 100%;
  padding: 0.5rem 0.7rem;
  border: 1.5px solid #CFE3C6;
  border-radius: 7px;
  margin-bottom: 0.5rem;
  font-size: 1rem;
}
.modal-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
  justify-content: flex-end;
}
.modal-actions button {
  padding: 0.6rem 1.2rem;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
  min-width: 100px;
  width: 100px;
}
.modal-actions button[type="submit"] {
  background: #4CB050;
  color: #fff;
}
.modal-actions button[type="submit"]:hover {
  background: #17635A;
}
.modal-actions button[type="button"] {
  background: #f0f0f0;
  color: #666;
}
.modal-actions button[type="button"]:hover {
  background: #e0e0e0;
  color: #333;
}
@media (max-width: 600px) {
  .admin-users, .modal {
    padding: 1rem 0.3rem;
  }
  table, th, td {
    font-size: 0.95rem;
  }
}
</style> 