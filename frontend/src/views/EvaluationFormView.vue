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
  max-width: 600px;
  margin: 1rem auto;
  width: 100%;
  box-sizing: border-box;
}

h2 {
  color: #17635A;
  font-size: 1.5rem;
  margin-bottom: 1.2rem;
  text-align: center;
}

.work-info {
  background: #CFE3C6;
  border-radius: 8px;
  padding: 1.2rem;
  margin-bottom: 1.5rem;
  color: #17635A;
  font-weight: 600;
  line-height: 1.6;
  word-wrap: break-word;
}

form {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

.criterion {
  display: flex;
  flex-direction: column;
}

.criterion label {
  color: #17635A;
  font-weight: 600;
  margin-bottom: 0.5rem;
  line-height: 1.4;
  display: block;
  text-align: justify;
  font-size: 0.95rem;
}

.criterion input {
  width: 100%;
  padding: 0.8rem 1rem;
  border: 1.5px solid #CFE3C6;
  border-radius: 7px;
  font-size: 1rem;
  box-sizing: border-box;
  transition: border 0.2s;
}

.criterion input:focus {
  border-color: #17635A;
  outline: none;
  box-shadow: 0 0 0 3px rgba(23, 99, 90, 0.1);
}

button {
  background: #4CB050;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 0.8rem 0;
  font-weight: 700;
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

.loading {
  color: #17635A;
  font-weight: 600;
  margin: 2rem 0;
  text-align: center;
  padding: 1rem;
}

@media (max-width: 768px) {
  .evaluation-form {
    padding: 1.5rem;
    margin: 0.5rem auto;
    max-width: 95%;
  }

  h2 {
    font-size: 1.3rem;
  }

  .work-info {
    padding: 1rem;
    font-size: 0.9rem;
  }

  .criterion label {
    font-size: 0.9rem;
  }

  .criterion input {
    padding: 0.7rem 0.8rem;
    font-size: 0.95rem;
  }

  button {
    padding: 0.7rem 0;
    font-size: 1rem;
  }
}

@media (max-width: 480px) {
  .evaluation-form {
    padding: 1rem;
    margin: 0.3rem auto;
    border-radius: 8px;
  }

  h2 {
    font-size: 1.2rem;
    margin-bottom: 1rem;
  }

  .work-info {
    padding: 0.8rem;
    font-size: 0.85rem;
    line-height: 1.5;
  }

  form {
    gap: 1rem;
  }

  .criterion label {
    font-size: 0.85rem;
    margin-bottom: 0.4rem;
  }

  .criterion input {
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

  .loading {
    font-size: 0.9rem;
  }
}

@media (max-width: 360px) {
  .evaluation-form {
    padding: 0.8rem;
    margin: 0.2rem auto;
  }

  h2 {
    font-size: 1.1rem;
  }

  .work-info {
    padding: 0.6rem;
    font-size: 0.8rem;
  }

  .criterion label {
    font-size: 0.8rem;
  }

  .criterion input {
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
