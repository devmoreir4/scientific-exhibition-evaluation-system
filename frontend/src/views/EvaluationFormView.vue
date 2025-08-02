<template>
  <div class="evaluation-form">
    <h2>Avaliação do Trabalho</h2>
    <div v-if="loadingWork" class="loading">Carregando dados do trabalho...</div>
    <div v-else-if="work">
      <div class="work-info">
        <strong>{{ work.title }}</strong> <br />
        <strong>Autores:</strong> {{ work.authors }}<br />
        <strong>Orientador:</strong> {{ work.advisor }}<br />
        <strong>Tipo:</strong> {{ getTypeLabel(work.type) }}<br />
        <strong>Área:</strong> {{ work.area }} | <strong>Subárea:</strong> {{ work.subarea }}
      </div>
      <form @submit.prevent="submitEvaluation">
        <div v-for="(criterion, index) in criteria" :key="index" class="criterion">
          <label :for="'criterion' + (index + 1)">{{ criterion }}</label>
          <input :id="'criterion' + (index + 1)" type="number" min="1" max="5" step="1" v-model.number="scores[index]" required />
        </div>
        <button type="submit" :disabled="submitting">{{ submitting ? 'Enviando...' : 'Enviar Avaliação' }}</button>
        <div v-if="successMsg" class="success">{{ successMsg }}</div>
        <div v-if="errorMsg" class="error">{{ errorMsg }}</div>
      </form>
    </div>
    <div v-else class="error">Trabalho não encontrado.</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../axios'

const route = useRoute()
const router = useRouter()
const workId = route.params.work_id
const work = ref(null)
const loadingWork = ref(true)
const scores = ref([1,1,1,1,1])
const submitting = ref(false)
const successMsg = ref('')
const errorMsg = ref('')

const criteria = [
  'Qualidade visual do pôster:',
  'Estrutura do pôster (introdução, métodos, resultados, conclusões):',
  'Relevância social, ambiental, cultural ou tecnológica:',
  'Criatividade e originalidade da proposta:',
  'Expressão oral (volume, clareza e pausa) e domínio do assunto (conceitos, linguagem e termos técnicos):'
]

function getTypeLabel(type) {
  const types = {
    'poster_banner': 'Pôster/Banner',
    'oral_presentation': 'Apresentação Oral'
  }
  return types[type] || type
}

function fetchWork() {
  loadingWork.value = true
  api.get(`/evaluator/works/${workId}`)
    .then(res => {
      if (res.data && res.data.work) {
        work.value = res.data.work
      } else {
        work.value = null
      }
    })
    .catch(() => { work.value = null })
    .finally(() => { loadingWork.value = false })
}

function submitEvaluation() {
  submitting.value = true
  successMsg.value = ''
  errorMsg.value = ''
  const payload = {
    work_id: Number(workId),
    criterion1: scores.value[0],
    criterion2: scores.value[1],
    criterion3: scores.value[2],
    criterion4: scores.value[3],
    criterion5: scores.value[4]
  }
  api.post('/evaluator/evaluations', payload)
    .then(() => {
      successMsg.value = 'Avaliação enviada com sucesso!'
      setTimeout(() => {
        router.push('/dashboard')
      }, 1500)
    })
    .catch(e => { errorMsg.value = e.response?.data?.msg || 'Erro ao enviar avaliação.' })
    .finally(() => { submitting.value = false })
}

onMounted(fetchWork)
</script>

<style scoped>
.evaluation-form {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px #17635a22;
  padding: 2rem;
  max-width: 500px;
  margin-left: auto;
  margin-right: auto;
}
h2 {
  color: #17635A;
  font-size: 1.5rem;
  margin-bottom: 1.2rem;
}
.work-info {
  background: #CFE3C6;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1.5rem;
  color: #17635A;
  font-weight: 600;
  line-height: 1.6;
}
form {
  display: flex;
  flex-direction: column;
  gap: 1.1rem;
}
.criterion label {
  color: #17635A;
  font-weight: 600;
  margin-bottom: 0.2rem;
  line-height: 1.4;
  display: block;
  text-align: justify;
}
.criterion input {
  width: 100%;
  padding: 0.5rem 0.7rem;
  border: 1.5px solid #CFE3C6;
  border-radius: 7px;
  font-size: 1rem;
  margin-top: 0.3rem;
}
button {
  background: #4CB050;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 0.7rem 0;
  font-weight: 700;
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
.loading {
  color: #17635A;
  font-weight: 600;
  margin: 2rem 0;
}
</style>
