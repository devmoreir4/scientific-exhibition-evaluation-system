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
            <th>Data de Nascimento</th>
            <th>Área</th>
            <th>Subáreas</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.name }}</td>
            <td>{{ user.siape_or_cpf }}</td>
            <td>{{ user.birthdate }}</td>
            <td>{{ user.area }}</td>
            <td>{{ user.subareas }}</td>
            <td>
              <button class="edit-btn" @click="openModal(user)">Editar</button>
              <button class="remove-btn" @click="removeUser(user.id)">Remover</button>
            </td>
          </tr>
        </tbody>
      </table>

      <Pagination
        v-if="pagination && pagination.total > 0"
        :pagination="pagination"
        @page-change="onPageChange"
        @per-page-change="onPerPageChange"
      />

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
          <select v-model="form.area" @change="onAreaChange" required>
            <option value="">Selecione uma área</option>
            <option v-for="area in availableAreas" :key="area" :value="area">{{ area }}</option>
          </select>
                    <label>
            Subáreas de Interesse
            <span v-if="form.area === 'Pedagógica'" class="hint">(pode avaliar qualquer subárea)</span>
          </label>
          <div v-if="form.area && availableSubareas.length > 0" class="subareas-select">
            <select multiple v-model="selectedSubareas" size="6" class="multi-select">
              <option v-for="subarea in availableSubareas" :key="subarea" :value="subarea">
                {{ subarea }}
              </option>
            </select>
            <div class="select-help">
              💡 Segure Ctrl/Cmd para selecionar múltiplas subáreas
            </div>
            <div v-if="selectedSubareas.length > 0" class="selected-preview">
              <strong>Selecionadas ({{ selectedSubareas.length }}):</strong>
              <div class="selected-tags">
                <span v-for="subarea in selectedSubareas" :key="subarea" class="tag">
                  {{ subarea }}
                  <button type="button" @click="removeSubarea(subarea)" class="tag-remove">×</button>
                </span>
              </div>
            </div>
          </div>
          <div v-else-if="form.area && availableSubareas.length === 0" class="info">
            Selecione uma área para ver as subáreas disponíveis
          </div>
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
import Pagination from '../components/Pagination.vue'

const users = ref([])
const loading = ref(true)
const error = ref('')
const pagination = ref(null)
const currentPage = ref(1)
const currentPerPage = ref(20)
const showModal = ref(false)
const editingUser = ref(null)
const modalError = ref('')
const form = reactive({ name: '', siape_or_cpf: '', area: '', subareas: '', birthdate: '' })

const availableAreas = ref([])
const availableSubareas = ref([])
const selectedSubareas = ref([])
const loadingAreas = ref(false)
const loadingSubareas = ref(false)

function fetchUsers() {
  loading.value = true
  error.value = ''
  const params = new URLSearchParams({
    page: currentPage.value.toString(),
    per_page: currentPerPage.value.toString()
  })

  api.get(`/admin/users?${params}`)
    .then(res => {
      users.value = res.data.users
      pagination.value = res.data.pagination
    })
    .catch(e => {
      console.error('Erro /admin/users:', e, e.response)
      error.value = e.response?.data?.msg || JSON.stringify(e.response?.data) || e.message || 'Erro ao buscar avaliadores.'
    })
    .finally(() => { loading.value = false })
}

function onPageChange(page) {
  currentPage.value = page
  fetchUsers()
}

function onPerPageChange(perPage) {
  currentPerPage.value = perPage
  currentPage.value = 1
  fetchUsers()
}

function fetchAreas() {
  loadingAreas.value = true
  api.get('/admin/areas')
    .then(res => {
      availableAreas.value = res.data.areas
    })
    .catch(e => {
      console.error('Erro ao buscar áreas:', e)
      modalError.value = 'Erro ao carregar áreas'
    })
    .finally(() => { loadingAreas.value = false })
}

function fetchSubareas(area) {
  if (!area) {
    availableSubareas.value = []
    return
  }

  loadingSubareas.value = true
  api.get(`/admin/areas/${encodeURIComponent(area)}/subareas`)
    .then(res => {
      availableSubareas.value = res.data.subareas
    })
    .catch(e => {
      console.error('Erro ao buscar subáreas:', e)
      availableSubareas.value = []
    })
    .finally(() => { loadingSubareas.value = false })
}

function openModal(user = null) {
  showModal.value = true
  editingUser.value = user
  fetchAreas()

  if (user) {
    Object.assign(form, user)
    selectedSubareas.value = user.subareas ? user.subareas.split(';').map(s => s.trim()) : []
    if (user.area) {
      fetchSubareas(user.area)
    }
  } else {
    Object.assign(form, { name: '', siape_or_cpf: '', area: '', subareas: '', birthdate: '' })
    selectedSubareas.value = []
    availableSubareas.value = []
  }
  modalError.value = ''
}

function closeModal() {
  showModal.value = false
  editingUser.value = null
  modalError.value = ''
  selectedSubareas.value = []
  availableSubareas.value = []
}

function onAreaChange() {
  selectedSubareas.value = []
  fetchSubareas(form.area)
}

function removeSubarea(subarea) {
  const index = selectedSubareas.value.indexOf(subarea)
  if (index > -1) {
    selectedSubareas.value.splice(index, 1)
  }
}

function saveUser() {
  modalError.value = ''

  if (selectedSubareas.value.length === 0) {
    modalError.value = 'Selecione pelo menos uma subárea'
    return
  }

  const payload = {
    ...form,
    subareas: selectedSubareas.value.join(';')
  }

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
}
h2 {
  color: #17635A;
  font-size: 1.5rem;
  margin-bottom: 1.2rem;
  text-align: center;
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
  min-width: 450px;
  max-width: 90vw;
  max-height: 90vh;
  overflow-y: auto;
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
.modal input, .modal select {
  width: 100%;
  padding: 0.5rem 0.7rem;
  border: 1.5px solid #CFE3C6;
  border-radius: 7px;
  margin-bottom: 0.5rem;
  font-size: 1rem;
}
.subareas-select {
  margin-bottom: 1rem;
}
.multi-select {
  width: 100%;
  border: 1.5px solid #CFE3C6;
  border-radius: 7px;
  padding: 0.5rem;
  font-size: 0.9rem;
  line-height: 1.4;
  background: #fff;
  resize: vertical;
  min-height: 120px;
}
.multi-select option {
  padding: 0.3rem 0.5rem;
  border-radius: 4px;
  margin: 1px 0;
}
.multi-select option:checked {
  background: #4CB050 !important;
  color: white !important;
}
.select-help {
  font-size: 0.8rem;
  color: #666;
  margin-top: 0.3rem;
  text-align: center;
  font-style: italic;
}
.selected-preview {
  margin-top: 0.8rem;
  padding: 0.8rem;
  background: #F5F6FA;
  border-radius: 6px;
  border: 1px solid #CFE3C6;
}
.selected-preview strong {
  color: #17635A;
  font-size: 0.9rem;
}
.selected-tags {
  margin-top: 0.5rem;
  display: flex;
  flex-wrap: wrap;
  gap: 0.3rem;
}
.tag {
  display: inline-flex;
  align-items: center;
  background: #4CB050;
  color: white;
  padding: 0.2rem 0.5rem;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: 500;
}
.tag-remove {
  background: none;
  border: none;
  color: white;
  margin-left: 0.3rem;
  cursor: pointer;
  font-weight: bold;
  font-size: 1rem;
  line-height: 1;
  padding: 0;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}
.tag-remove:hover {
  background: rgba(255,255,255,0.2);
}
.hint {
  font-size: 0.8rem;
  color: #666;
  font-weight: normal;
  font-style: italic;
}
.info {
  color: #666;
  font-style: italic;
  margin-bottom: 0.5rem;
  padding: 0.5rem;
  background: #F5F6FA;
  border-radius: 6px;
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

</style>
