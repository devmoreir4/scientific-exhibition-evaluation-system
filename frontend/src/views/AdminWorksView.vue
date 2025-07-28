<template>
  <div class="admin-works">
    <h2>Trabalhos</h2>
    <div v-if="loading" class="loading">Carregando trabalhos...</div>
    <div v-else>
      <table>
        <thead>
          <tr>
            <th>Título</th>
            <th>Autor</th>
            <th>Área</th>
            <th>Subárea</th>
            <th>Resumo</th>
            <th>Estudante Técnico</th>
            <th>Protótipo</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="work in works" :key="work.id">
            <td>{{ work.title }}</td>
            <td>{{ work.author }}</td>
            <td>{{ work.area }}</td>
            <td>{{ work.subarea }}</td>
            <td>{{ work.abstract }}</td>
            <td>{{ work.has_technical_student ? 'Sim' : 'Não' }}</td>
            <td>{{ work.has_prototype ? 'Sim' : 'Não' }}</td>
            <td>
              <button class="edit-btn" @click="openModal(work)">Editar</button>
              <button class="remove-btn" @click="removeWork(work.id)">Remover</button>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-if="error" class="error">{{ error }}</div>
    </div>

    <div v-if="showModal" class="modal-bg">
      <div class="modal">
        <h3>Editar Trabalho</h3>
        <form @submit.prevent="saveWork">
          <label>Título</label>
          <input v-model="form.title" required />
          <label>Autor</label>
          <input v-model="form.author" required />
          <label>Área</label>
          <input v-model="form.area" required />
          <label>Subárea</label>
          <input v-model="form.subarea" required />
          <label>Resumo</label>
          <textarea v-model="form.abstract" required rows="3" />
          <label>
            <input type="checkbox" v-model="form.has_technical_student" /> Estudante Técnico
          </label>
          <label>
            <input type="checkbox" v-model="form.has_prototype" /> Protótipo
          </label>
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

const works = ref([])
const loading = ref(true)
const error = ref('')
const showModal = ref(false)
const editingWork = ref(null)
const modalError = ref('')
const form = reactive({ title: '', author: '', area: '', subarea: '', abstract: '', has_technical_student: false, has_prototype: false })

function fetchWorks() {
  loading.value = true
  error.value = ''
  api.get('/admin/works')
    .then(res => { 
      console.log('Resposta /admin/works:', res)
      works.value = res.data.works 
    })
    .catch(e => { 
      console.error('Erro /admin/works:', e, e.response)
      error.value = e.response?.data?.msg || JSON.stringify(e.response?.data) || e.message || 'Erro ao buscar trabalhos.' 
    })
    .finally(() => { loading.value = false })
}

function openModal(work) {
  showModal.value = true
  editingWork.value = work
  Object.assign(form, work)
  modalError.value = ''
}

function closeModal() {
  showModal.value = false
  editingWork.value = null
  modalError.value = ''
}

function saveWork() {
  modalError.value = ''
  const payload = { ...form }
  api.put(`/admin/works/${editingWork.value.id}`, payload)
    .then(() => { fetchWorks(); closeModal() })
    .catch(e => { modalError.value = e.response?.data?.msg || 'Erro ao editar trabalho.' })
}

function removeWork(id) {
  if (!confirm('Tem certeza que deseja remover este trabalho?')) return
  api.delete(`/admin/works/${id}`)
    .then(() => fetchWorks())
    .catch(e => { error.value = e.response?.data?.msg || 'Erro ao remover trabalho.' })
}

onMounted(fetchWorks)
</script>

<style scoped>
.admin-works {
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
.modal input, .modal textarea {
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
@media (max-width: 600px) {
  .admin-works, .modal {
    padding: 1rem 0.3rem;
  }
  table, th, td {
    font-size: 0.95rem;
  }
}
</style> 