<template>
  <div class="admin-sheets">
    <h2>Distribuição de Trabalhos</h2>
    <button class="distribute-btn" @click="distributeWorks" :disabled="distributing || isDistributed || checkingStatus">
      {{
        checkingStatus ? 'Verificando Status...' :
        distributing ? 'Distribuindo...' :
        isDistributed ? 'Distribuição Realizada' :
        'Distribuir Trabalhos'
      }}
    </button>
    <div v-if="distMsg" class="success">{{ distMsg }}</div>
    <div v-if="distError" class="error">{{ distError }}</div>

    <h2 style="margin-top:1.5rem">Processar Ficha Manual (OCR/IA)</h2>
    <form @submit.prevent="processSheetAi" class="upload-form">
      <div class="file-input-wrapper">
        <input type="file" @change="onFileChange" accept="image/*" required id="file-input" />
        <label for="file-input" class="file-input-label">
          <span v-if="!file">Escolher Imagem</span>
          <span v-else>{{ file.name }}</span>
        </label>
      </div>
      <button type="submit" :disabled="processing">{{ processing ? 'Processando...' : 'Enviar Ficha' }}</button>
    </form>
    <div v-if="processMsg" class="success">{{ processMsg }}</div>
    <div v-if="processError" class="error">{{ processError }}</div>

    <div v-if="lastSheet" class="sheet-preview">
      <h3>Última Ficha Processada</h3>

      <div class="sheet-data">
        <h4>Dados Extraídos (Editáveis)</h4>
        <form @submit.prevent="confirmSheet" class="confirmation-form">
          <div class="form-group">
            <label>Avaliador:</label>
            <select v-model="formData.evaluator_id" @change="onEvaluatorChange" required>
              <option value="">Selecione um avaliador</option>
              <option v-for="evaluator in evaluators" :key="evaluator.id" :value="evaluator.id">
                {{ evaluator.name }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label>Trabalho:</label>
            <select v-model="formData.work_id" required :disabled="!formData.evaluator_id || loadingFilteredWorks">
              <option value="">{{ loadingFilteredWorks ? 'Carregando...' : 'Selecione um trabalho' }}</option>
              <option v-for="work in filteredWorks" :key="work.id" :value="work.id">
                {{ work.title }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label>Critérios (1-5):</label>
            <div class="criteria-inputs">
              <input
                v-for="(score, index) in formData.scores"
                :key="index"
                type="number"
                v-model.number="formData.scores[index]"
                min="1"
                max="5"
                required
                :placeholder="`Critério ${index + 1}`"
              />
            </div>
          </div>
          <div class="form-actions">
            <button type="submit" :disabled="confirming">
              {{ confirming ? 'Confirmando...' : 'Confirmar Avaliação' }}
            </button>
          </div>
        </form>
      </div>

      <div v-if="confirmMsg" class="success">{{ confirmMsg }}</div>
      <div v-if="confirmError" class="error">{{ confirmError }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../axios'

const router = useRouter()

const distributing = ref(false)
const distMsg = ref('')
const distError = ref('')
const isDistributed = ref(false)
const checkingStatus = ref(false)

const processing = ref(false)
const processMsg = ref('')
const processError = ref('')
const file = ref(null)
const lastSheet = ref(null)
const lastSheetImgUrl = ref('')

const confirming = ref(false)
const confirmMsg = ref('')
const confirmError = ref('')

const evaluators = ref([])
const loadingEvaluators = ref(false)
const works = ref([])
const loadingWorks = ref(false)
const filteredWorks = ref([])
const loadingFilteredWorks = ref(false)

const formData = reactive({
  work_id: '',
  evaluator_id: '',
  scores: [1, 1, 1, 1, 1]
})

function fetchEvaluators() {
  loadingEvaluators.value = true
  api.get('/admin/users/simple')
    .then(res => {
      evaluators.value = res.data.users
    })
    .catch(e => {
      console.error('Erro ao buscar avaliadores:', e)
    })
    .finally(() => {
      loadingEvaluators.value = false
    })
}

function fetchWorks() {
  loadingWorks.value = true
  api.get('/admin/works')
    .then(res => {
      works.value = res.data.works
    })
    .catch(e => {
      console.error('Erro ao buscar trabalhos:', e)
    })
    .finally(() => {
      loadingWorks.value = false
    })
}

function fetchWorksByEvaluator(evaluatorId) {
  if (!evaluatorId) {
    filteredWorks.value = []
    return
  }

  loadingFilteredWorks.value = true
  api.get(`/admin/works/evaluator/${evaluatorId}`)
    .then(res => {
      filteredWorks.value = res.data.works
    })
    .catch(e => {
      console.error('Erro ao buscar trabalhos do avaliador:', e)
      filteredWorks.value = []
    })
    .finally(() => {
      loadingFilteredWorks.value = false
    })
}

function onEvaluatorChange() {
  formData.work_id = ''
  fetchWorksByEvaluator(formData.evaluator_id)
}

function checkDistributionStatus() {
  checkingStatus.value = true
  return api.get('/admin/works/distribution-status')
    .then(res => {
      isDistributed.value = res.data.distributed
    })
    .catch(e => {
      console.error('Erro ao verificar status da distribuição:', e)
      // erro = não distribuído
      isDistributed.value = false
    })
    .finally(() => {
      checkingStatus.value = false
    })
}

function distributeWorks() {
  distributing.value = true
  distMsg.value = ''
  distError.value = ''
  api.post('/admin/works/distribute')
    .then(res => {
      distMsg.value = 'Distribuição realizada com sucesso!'
      isDistributed.value = true
    })
    .catch(e => {
      console.error('Erro /admin/works/distribute:', e, e.response)
      distError.value = e.response?.data?.msg || JSON.stringify(e.response?.data) || e.message || 'Erro ao distribuir trabalhos.'
    })
    .finally(() => { distributing.value = false })
}

function onFileChange(e) {
  file.value = e.target.files[0]
}

function processSheetAi() {
  if (!file.value) return
  processing.value = true
  processMsg.value = ''
  processError.value = ''
  const uploadFormData = new FormData()
  uploadFormData.append('file', file.value)
  api.post('/admin/sheets/process-ai', uploadFormData)
    .then(res => {
      // console.log('Resposta /admin/sheets/process-ai:', res)
      // console.log('Dados extraídos:', res.data)

      lastSheet.value = res.data
      if (res.data.saved_image) {
        lastSheetImgUrl.value = `/uploads/${res.data.saved_image}`
      }

      formData.work_id = ''
      formData.evaluator_id = ''
      filteredWorks.value = []

      const extractedScores = res.data.extracted_scores || []
      formData.scores = extractedScores.map(score => {
        if (score === null || score === undefined) {
          return 1
        }
        const numScore = parseInt(score)
        return (numScore && numScore >= 1 && numScore <= 5) ? numScore : 1
      })

      while (formData.scores.length < 5) {
        formData.scores.push(1)
      }

      const allNullScores = extractedScores.every(score => score === null || score === undefined)

      if (allNullScores) {
        processError.value = 'Atenção: Nenhuma marca válida foi encontrada.'
      } else if (res.data.warning) {
        processMsg.value = 'Ficha processada, mas com avisos: ' + res.data.warning
      } else {
        processMsg.value = 'Ficha processada com sucesso!'
      }
    })
    .catch(e => {
      console.error('Erro /admin/sheets/process-ai:', e, e.response)
      processError.value = e.response?.data?.msg || JSON.stringify(e.response?.data) || e.message || 'Erro ao processar ficha.'
    })
    .finally(() => { processing.value = false })
}

function confirmSheet() {
  if (!lastSheet.value) return

  if (!formData.work_id) {
    confirmError.value = 'Por favor, selecione um trabalho.'
    return
  }

  if (!formData.evaluator_id) {
    confirmError.value = 'Por favor, selecione um avaliador.'
    return
  }

  const selectedWork = works.value.find(w => w.id === formData.work_id)
  if (!selectedWork) {
    confirmError.value = 'Trabalho selecionado não encontrado na lista.'
    return
  }

  const selectedEvaluator = evaluators.value.find(e => e.id === formData.evaluator_id)
  if (!selectedEvaluator) {
    confirmError.value = 'Avaliador selecionado não encontrado na lista.'
    return
  }

  for (let i = 0; i < formData.scores.length; i++) {
    const score = formData.scores[i]
    if (!score || isNaN(score) || score < 1 || score > 5) {
      confirmError.value = `Critério ${i + 1} deve ser um número entre 1 e 5.`
      return
    }
  }

  confirming.value = true
  confirmMsg.value = ''
  confirmError.value = ''

  const payload = {
    work_id: parseInt(formData.work_id),
    evaluator_id: parseInt(formData.evaluator_id),
    scores: formData.scores
  }

  api.post('/admin/sheets/confirm', payload)
    .then(() => {
      confirmMsg.value = 'Avaliação manual confirmada com sucesso!'
      setTimeout(() => {
        router.push('/admin/dashboard')
      }, 1500)
    })
    .catch(e => { confirmError.value = e.response?.data?.msg || 'Erro ao confirmar avaliação.' })
    .finally(() => { confirming.value = false })
}

onMounted(async () => {
  await checkDistributionStatus()

  fetchEvaluators()
  fetchWorks()
})
</script>

<style scoped>
.admin-sheets {
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
.distribute-btn {
  background: #4CB050;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 0.5rem 1.2rem;
  font-weight: 700;
  margin-bottom: 1.2rem;
  cursor: pointer;
  transition: background 0.2s;
  display: block;
  margin-left: auto;
  margin-right: auto;
}
.distribute-btn:hover {
  background: #17635A;
}
.distribute-btn:disabled {
  background: #CFE3C6;
  color: #17635A;
  opacity: 0.7;
}
.upload-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  align-items: center;
  margin-bottom: 1.2rem;
  max-width: 400px;
  margin: auto;
}

.upload-form button {
  background: #17635A;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 0.5rem 1.2rem;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.2s;
  width: 100%;
  max-width: 180px;
  height: 38px;
}
.upload-form button:disabled {
  background: #CFE3C6;
  color: #17635A;
  opacity: 0.7;
}
.file-input-wrapper {
  position: relative;
  min-width: 180px;
  height: 38px;
  border: 1.5px solid #CFE3C6;
  border-radius: 8px;
  overflow: hidden;
  display: flex;
  align-items: center;
  padding: 0 10px;
  background: #F5F6FA;
  cursor: pointer;
  transition: border-color 0.2s, background 0.2s;
}
.file-input-wrapper:hover {
  border-color: #4CB050;
  background: #fff;
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
.file-input-label span {
  transition: opacity 0.2s ease-in-out;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
}
.success {
  color: #4CB050;
  margin-top: 1rem;
  font-weight: 600;
  text-align: center;
  padding: 0.8rem;
  background: rgba(76, 176, 80, 0.1);
  border-radius: 6px;
}
.error {
  color: #b00020;
  margin-top: 1rem;
  font-weight: 600;
  text-align: center;
  padding: 0.8rem;
  background: rgba(176, 0, 32, 0.1);
  border-radius: 6px;
}
.sheet-preview {
  margin-top: 2rem;
  background: #F5F6FA;
  border-radius: 10px;
  padding: 1.2rem;
  box-shadow: 0 1px 6px #17635a11;
}
.sheet-preview img {
  max-width: 220px;
  border-radius: 8px;
  margin-bottom: 1rem;
  display: block;
}
.sheet-data {
  background: #fff;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1rem;
}
.sheet-data h4 {
  color: #17635A;
  margin-bottom: 1rem;
  font-size: 1.1rem;
}
.confirmation-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.form-group label {
  color: #17635A;
  font-weight: 600;
  font-size: 0.95rem;
}
.form-group input, .form-group select {
  padding: 0.5rem 0.7rem;
  border: 1.5px solid #CFE3C6;
  border-radius: 6px;
  font-size: 1rem;
}
.criteria-inputs {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}
.criteria-inputs input {
  width: 60px;
  text-align: center;
}
.form-actions {
  margin-top: 1rem;
}
.form-actions button {
  background: #4CB050;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 0.7rem 1.5rem;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.2s;
}
.form-actions button:disabled {
  background: #CFE3C6;
  color: #17635A;
  opacity: 0.7;
}

</style>
