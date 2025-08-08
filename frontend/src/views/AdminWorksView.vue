<template>
  <div class="admin-works">
    <h2>Trabalhos</h2>

    <!-- Seção de Importação CSV -->
          <div class="import-section">
            <h3>Importar Trabalhos</h3>
            <div class="import-info">
         </div>

          <form @submit.prevent="importCsv" class="import-form">
           <div class="file-input-wrapper">
             <input type="file" @change="onCsvFileChange" accept=".csv" required id="csv-file-input" />
             <label for="csv-file-input" class="file-input-label">
               <span v-if="!selectedFile">Escolher arquivo (.csv)</span>
               <span v-else>{{ selectedFile.name }}</span>
             </label>
           </div>
           <button type="submit" :disabled="importing">
             {{ importing ? 'Importando...' : 'Importar CSV' }}
           </button>
          </form>

      <div v-if="importMsg" class="success">{{ importMsg }}</div>
      <div v-if="importError" class="error">{{ importError }}</div>

      <!-- Lista de áreas disponíveis -->
      <details class="areas-list">
        <summary>Ver áreas e subáreas disponíveis</summary>
        <div class="areas-content">
          <div v-for="(subareas, area) in availableAreas" :key="area" class="area-group">
            <h4>{{ area }}</h4>
            <ul>
              <li v-for="subarea in subareas" :key="subarea">{{ subarea }}</li>
            </ul>
          </div>
        </div>
      </details>
    </div>

    <!-- Lista de Trabalhos -->
    <div class="works-section">
      <h3>Lista de Trabalhos</h3>
      <div v-if="loading" class="loading">Carregando trabalhos...</div>
      <div v-else>
        <table>
          <thead>
            <tr>
              <th>Título</th>
              <th>Autores</th>
              <th>Orientador</th>
              <th>Tipo</th>
              <th>Área</th>
              <th>Subárea</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="work in works" :key="work.id">
              <td>{{ work.title }}</td>
              <td>{{ work.authors }}</td>
              <td>{{ work.advisor }}</td>
              <td>{{ getTypeLabel(work.type) }}</td>
              <td>{{ work.area }}</td>
              <td>{{ work.subarea }}</td>
              <td>
                <button class="edit-btn" @click="openModal(work)">Editar</button>
                <button class="remove-btn" @click="removeWork(work.id)">Remover</button>
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
    </div>

    <div v-if="showModal" class="modal-bg">
      <div class="modal">
        <h3>Editar Trabalho</h3>
        <form @submit.prevent="saveWork">
          <label>Título</label>
          <input v-model="form.title" required />
          <label>Autores</label>
          <input v-model="form.authors" required placeholder="Separados por ponto e vírgula (;)" />
          <label>Orientador</label>
          <input v-model="form.advisor" required />
          <label>Tipo</label>
          <select v-model="form.type" required>
            <option value="poster_banner">Pôster/Banner</option>
            <option value="oral_presentation">Apresentação Oral</option>
          </select>
          <label>Área</label>
          <input v-model="form.area" required />
          <label>Subárea</label>
          <input v-model="form.subarea" required />
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

const works = ref([])
const loading = ref(true)
const error = ref('')
const pagination = ref(null)
const currentPage = ref(1)
const currentPerPage = ref(20)
const showModal = ref(false)
const editingWork = ref(null)
const modalError = ref('')
const form = reactive({
  title: '',
  authors: '',
  advisor: '',
  type: 'poster_banner',
  area: '',
  subarea: ''
})

const selectedFile = ref(null)
const importing = ref(false)
const importMsg = ref('')
const importError = ref('')

const availableAreas = {
  'Ciências Agrárias': [
    'Agricultura e Sustentabilidade no Campo',
    'Zootecnia e Produção Animal',
    'Agroindústria e Alimentos',
    'Recursos Naturais e Meio Ambiente Rural',
    'Tecnologias e Processos Agrícolas'
  ],
  'Ciências Biológicas e Ciências da Saúde': [
    'Biotecnologia e Microbiologia',
    'Ecologia e Conservação',
    'Saúde Coletiva e Educação em Saúde',
    'Nutrição, Enfermagem e Bem-estar',
    'Práticas Integrativas e Promoção da Saúde'
  ],
  'Ciências Exatas e da Terra e Engenharias': [
    'Matemática, Física e Química Aplicada',
    'Tecnologias da Informação e Programação',
    'Robótica, Automação e Eletrônica',
    'Engenharia e Energias Renováveis',
    'Geociências e Sustentabilidade Ambiental'
  ],
  'Ciências Sociais Aplicadas e Ciências Humanas': [
    'História, Filosoa e Sociologia',
    'Geografia e Estudos Regionais',
    'Educação, Cidadania e Direitos Humanos',
    'Gestão, Empreendedorismo e Economia',
    'Comunicação, Informação e Cultura Digital'
  ],
  'Linguística, Letras e Artes': [
    'Língua Portuguesa e Produção Textual',
    'Línguas Estrangeiras e Multilinguismo',
    'Literatura, Leitura e Narrativas',
    'Artes Visuais, Dança e Teatro',
    'Música, Cinema e Audiovisual'
  ]
}

function getTypeLabel(type) {
  const types = {
    'poster_banner': 'Pôster/Banner',
    'oral_presentation': 'Apresentação Oral'
  }
  return types[type] || type
}

function onCsvFileChange(e) {
  selectedFile.value = e.target.files[0]
  importMsg.value = ''
  importError.value = ''
}

function importCsv() {
  if (!selectedFile.value) return

  importing.value = true
  importMsg.value = ''
  importError.value = ''

  const formData = new FormData()
  formData.append('file', selectedFile.value)

  api.post('/admin/works/import-csv', formData)
    .then(res => {
      importMsg.value = res.data.msg
      if (res.data.imported_count > 0) {
        fetchWorks()
      }
      selectedFile.value = null

      const fileInput = document.getElementById('csv-file-input')
      if (fileInput) fileInput.value = ''
    })
    .catch(e => {
      importError.value = e.response?.data?.msg || 'Erro ao importar CSV'
      if (e.response?.data?.errors) {
        importError.value += '\n\nErros detalhados:\n' + e.response.data.errors.join('\n')
      }
    })
    .finally(() => {
      importing.value = false
    })
}

function fetchWorks() {
  loading.value = true
  error.value = ''
  const params = new URLSearchParams({
    page: currentPage.value.toString(),
    per_page: currentPerPage.value.toString()
  })

  api.get(`/admin/works?${params}`)
    .then(res => {
      works.value = res.data.works
      pagination.value = res.data.pagination
    })
    .catch(e => {
      console.error('Erro /admin/works:', e, e.response)
      error.value = e.response?.data?.msg || JSON.stringify(e.response?.data) || e.message || 'Erro ao buscar trabalhos.'
    })
    .finally(() => { loading.value = false })
}

function onPageChange(page) {
  currentPage.value = page
  fetchWorks()
}

function onPerPageChange(perPage) {
  currentPerPage.value = perPage
  currentPage.value = 1
  fetchWorks()
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
}
h2 {
  color: #17635A;
  font-size: 1.5rem;
  margin-bottom: 1.2rem;
  text-align: center;
}
h3 {
  color: #17635A;
  font-size: 1.2rem;
  margin-bottom: 1rem;
}
.import-section {
  background: #F5F6FA;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  border: 1px solid #CFE3C6;
}
.import-info {
  margin-bottom: 1rem;
  font-size: 0.9rem;
  color: #666;
}
.import-info p {
  margin-bottom: 0.5rem;
}
.import-form {
  display: flex;
  gap: 1rem;
  align-items: center;
  margin-bottom: 1rem;
}
.file-input-wrapper {
  position: relative;
  min-width: 200px;
  height: 38px;
  border: 1.5px solid #CFE3C6;
  border-radius: 8px;
  overflow: hidden;
  display: flex;
  align-items: center;
  padding: 0 10px;
  background: #fff;
  cursor: pointer;
  transition: border-color 0.2s;
}
.file-input-wrapper:hover {
  border-color: #4CB050;
}
.file-input-wrapper input[type="file"] {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  cursor: pointer;
}
.file-input-label {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.9rem;
  color: #17635A;
  pointer-events: none;
  font-weight: 500;
}
.import-form button {
  background: #4CB050;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 0.5rem 1.2rem;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.2s;
}
.import-form button:hover {
  background: #17635A;
}
.import-form button:disabled {
  background: #CFE3C6;
  color: #17635A;
  opacity: 0.7;
}
.areas-list {
  margin-top: 1rem;
}
.areas-list summary {
  cursor: pointer;
  color: #17635A;
  font-weight: 600;
  padding: 0.5rem 0;
}
.areas-content {
  margin-top: 1rem;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1rem;
}
.area-group h4 {
  color: #17635A;
  margin-bottom: 0.5rem;
  font-size: 1rem;
}
.area-group ul {
  list-style: none;
  padding-left: 0;
}
.area-group li {
  padding: 0.2rem 0;
  color: #666;
  font-size: 0.9rem;
}
.works-section {
  margin-top: 2rem;
}
table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 1rem;
  font-size: 0.9rem;
}
th, td {
  padding: 0.5rem 0.3rem;
  text-align: left;
  vertical-align: top;
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
.success {
  color: #4CB050;
  margin-top: 1rem;
  font-weight: 600;
}
.error {
  color: #b00020;
  margin-top: 1rem;
  font-weight: 600;
  white-space: pre-line;
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
.modal input, .modal textarea, .modal select {
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
