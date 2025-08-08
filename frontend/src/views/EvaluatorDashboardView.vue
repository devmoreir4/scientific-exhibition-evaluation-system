<template>
  <div class="evaluator-dashboard">
    <h2>Trabalhos Atribuídos</h2>
    <div v-if="loadingWorks" class="loading">Carregando trabalhos...</div>
    <div v-else>
      <div v-if="works.length" class="works-container">
        <table class="works-table">
          <thead>
            <tr>
              <th>Título</th>
              <th>Autores</th>
              <th>Avaliar</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="work in works" :key="work.id">
              <td class="work-title">{{ work.title }}</td>
              <td class="work-authors">{{ work.authors }}</td>
              <td class="work-action">
                <router-link v-if="!isWorkEvaluated(work.id)" :to="`/evaluate/${work.id}`" class="eval-btn">Avaliar</router-link>
                <span v-else class="evaluated-badge">Avaliado</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else class="empty">Nenhum trabalho atribuído.</div>
      <div v-if="worksError" class="error">{{ worksError }}</div>
    </div>

    <h2 class="section-title">Minhas Avaliações</h2>
    <div v-if="loadingEvals" class="loading">Carregando avaliações...</div>
    <div v-else>
      <div v-if="evaluations.length" class="evaluations-container">
        <table class="evaluations-table">
          <thead>
            <tr>
              <th>Trabalho</th>
              <th>Critérios</th>
              <th>Método</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="evaluation in evaluations" :key="evaluation.id">
              <td class="eval-work-title">{{ evaluation.work_title }}</td>
              <td class="eval-criteria">{{ evaluation.criterion1 }}, {{ evaluation.criterion2 }}, {{ evaluation.criterion3 }}, {{ evaluation.criterion4 }}, {{ evaluation.criterion5 }}</td>
              <td class="eval-method">{{ getMethodLabel(evaluation.method) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else class="empty">Nenhuma avaliação realizada.</div>
      <div v-if="evalsError" class="error">{{ evalsError }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../axios'

const works = ref([])
const loadingWorks = ref(true)
const worksError = ref('')

const evaluations = ref([])
const loadingEvals = ref(true)
const evalsError = ref('')

function getMethodLabel(method) {
  const methods = {
    'online': 'Online',
    'manual_validated': 'Manual'
  }
  return methods[method] || method
}

function isWorkEvaluated(workId) {
  return evaluations.value.some(evaluation => evaluation.work_id === workId)
}

function fetchWorks() {
  loadingWorks.value = true
  worksError.value = ''
  api.get('/evaluator/works/assigned')
    .then(res => { works.value = res.data.works })
    .catch(e => { worksError.value = e.response?.data?.msg || 'Erro ao buscar trabalhos.' })
    .finally(() => { loadingWorks.value = false })
}

function fetchEvals() {
  loadingEvals.value = true
  evalsError.value = ''
  api.get('/evaluator/evaluations/mine')
    .then(res => { evaluations.value = res.data.evaluations })
    .catch(e => { evalsError.value = e.response?.data?.msg || 'Erro ao buscar avaliações.' })
    .finally(() => { loadingEvals.value = false })
}

onMounted(() => {
  fetchWorks()
  fetchEvals()
})
</script>

<style scoped>
.evaluator-dashboard {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px #17635a22;
  padding: 2rem;
  margin: 1rem;
}

h2 {
  color: #17635A;
  font-size: 1.5rem;
  margin-bottom: 1.2rem;
  font-weight: 700;
}

.section-title {
  margin-top: 2rem;
}

.works-container,
.evaluations-container {
  overflow-x: auto;
  margin-bottom: 1rem;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 1rem;
  font-size: 0.9rem;
  min-width: 400px;
}

th, td {
  padding: 0.8rem 0.5rem;
  text-align: left;
  vertical-align: top;
  border-bottom: 1px solid #eee;
}

th {
  background: #CFE3C6;
  color: #17635A;
  font-weight: 800;
  position: sticky;
  top: 0;
  z-index: 10;
}

tbody tr:nth-child(even) {
  background: #F5F6FA;
}

tbody tr:hover {
  background: #e8f5e8;
}

.work-title,
.eval-work-title {
  font-weight: 600;
  max-width: 400px;
  word-wrap: break-word;
}

.work-authors {
  max-width: 300px;
  word-wrap: break-word;
}

.eval-method {
  max-width: 200px;
  word-wrap: break-word;
}

.eval-criteria {
  max-width: 400px;
  word-wrap: break-word;
}

.work-action {
  text-align: center;
  min-width: 100px;
}

.eval-btn {
  background: #4CB050;
  color: #fff;
  border: none;
  border-radius: 6px;
  padding: 0.4rem 0.8rem;
  font-weight: 600;
  text-decoration: none;
  transition: background 0.2s, color 0.2s;
  min-width: 80px;
  width: 80px;
  text-align: center;
  display: inline-block;
  box-sizing: border-box;
  font-size: 0.85rem;
}

.eval-btn:hover {
  background: #17635A;
  color: #fff;
}

.evaluated-badge {
  color: #4CB050;
  font-weight: 600;
  font-size: 0.85rem;
  display: inline-block;
  text-align: center;
  min-width: 80px;
  width: 80px;
  box-sizing: border-box;
  padding: 0.4rem 0;
}

.loading {
  color: #17635A;
  font-weight: 600;
  margin: 1rem 0;
  text-align: center;
  padding: 1rem;
}

.error {
  color: #b00020;
  margin-top: 1rem;
  font-weight: 600;
  padding: 0.5rem;
  background: rgba(176, 0, 32, 0.1);
  border-radius: 6px;
}

.empty {
  color: #888;
  margin: 1.5rem 0;
  font-style: italic;
  text-align: center;
  padding: 1rem;
}

@media (max-width: 1024px) {
  .evaluator-dashboard {
    padding: 1.5rem;
    margin: 0.5rem;
  }

  h2 {
    font-size: 1.3rem;
  }

  table {
    font-size: 0.85rem;
    min-width: 300px;
  }

  th, td {
    padding: 0.6rem 0.4rem;
  }

  .work-title,
  .eval-work-title {
    max-width: 300px;
  }

  .work-authors {
    max-width: 250px;
  }

  .eval-method {
    max-width: 150px;
  }

  .eval-criteria {
    max-width: 300px;
  }
}

@media (max-width: 768px) {
  .evaluator-dashboard {
    padding: 1rem;
    margin: 0.5rem;
    border-radius: 8px;
  }

  h2 {
    font-size: 1.2rem;
    margin-bottom: 1rem;
  }

  .section-title {
    margin-top: 1.5rem;
  }

  table {
    font-size: 0.8rem;
    min-width: 250px;
  }

  th, td {
    padding: 0.5rem 0.3rem;
  }

  .work-title,
  .eval-work-title {
    max-width: 250px;
  }

  .work-authors {
    max-width: 200px;
  }

  .eval-method {
    max-width: 120px;
  }

  .eval-criteria {
    max-width: 250px;
  }

  .eval-btn,
  .evaluated-badge {
    min-width: 70px;
    width: 70px;
    font-size: 0.8rem;
    padding: 0.3rem 0.6rem;
  }
}

@media (max-width: 480px) {
  .evaluator-dashboard {
    padding: 0.8rem;
    margin: 0.3rem;
  }

  h2 {
    font-size: 1.1rem;
    margin-bottom: 0.8rem;
  }

  table {
    font-size: 0.75rem;
    min-width: 200px;
  }

  th, td {
    padding: 0.4rem 0.2rem;
  }

  .work-title,
  .eval-work-title {
    max-width: 200px;
  }

  .work-authors {
    max-width: 150px;
  }

  .eval-method {
    max-width: 100px;
  }

  .eval-criteria {
    max-width: 200px;
  }

  .eval-btn,
  .evaluated-badge {
    min-width: 60px;
    width: 60px;
    font-size: 0.75rem;
    padding: 0.25rem 0.5rem;
  }

  .loading,
  .error,
  .empty {
    font-size: 0.9rem;
    padding: 0.8rem;
  }
}
</style>
