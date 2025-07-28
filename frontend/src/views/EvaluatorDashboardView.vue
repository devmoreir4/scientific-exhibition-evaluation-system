<template>
  <div class="evaluator-dashboard">
    <h2>Trabalhos Atribuídos</h2>
    <div v-if="loadingWorks" class="loading">Carregando trabalhos...</div>
    <div v-else>
      <table v-if="works.length">
        <thead>
          <tr>
            <th>Título</th>
            <th>Autores</th>
            <th>Orientador</th>
            <th>Tipo</th>
            <th>Área</th>
            <th>Subárea</th>
            <th>Avaliar</th>
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
              <router-link :to="`/evaluate/${work.id}`" class="eval-btn">Avaliar</router-link>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-else class="empty">Nenhum trabalho atribuído.</div>
      <div v-if="worksError" class="error">{{ worksError }}</div>
    </div>

    <h2 style="margin-top:2.5rem">Minhas Avaliações</h2>
    <div v-if="loadingEvals" class="loading">Carregando avaliações...</div>
    <div v-else>
      <table v-if="evaluations.length">
        <thead>
          <tr>
            <th>Trabalho</th>
            <th>Critérios</th>
            <th>Método</th>
            <th>Ver</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="evaluation in evaluations" :key="evaluation.id">
            <td>{{ evaluation.work_title }}</td>
            <td>{{ evaluation.criterion1 }}, {{ evaluation.criterion2 }}, {{ evaluation.criterion3 }}, {{ evaluation.criterion4 }}, {{ evaluation.criterion5 }}</td>
            <td>{{ getMethodLabel(evaluation.method) }}</td>
            <td>
              <router-link :to="`/evaluate/${evaluation.work_id}`" class="view-btn">Ver</router-link>
            </td>
          </tr>
        </tbody>
      </table>
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

function getTypeLabel(type) {
  const types = {
    'poster_banner': 'Pôster/Banner',
    'oral_presentation': 'Apresentação Oral'
  }
  return types[type] || type
}

function getMethodLabel(method) {
  const methods = {
    'online': 'Online',
    'manual_validated': 'Manual Validado'
  }
  return methods[method] || method
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
.eval-btn, .view-btn {
  background: #4CB050;
  color: #fff;
  border: none;
  border-radius: 6px;
  padding: 0.3rem 0.8rem;
  font-weight: 600;
  text-decoration: none;
  transition: background 0.2s, color 0.2s;
}
.eval-btn:hover, .view-btn:hover {
  background: #17635A;
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
.empty {
  color: #888;
  margin: 1.5rem 0;
  font-style: italic;
}
@media (max-width: 600px) {
  .evaluator-dashboard {
    padding: 1rem 0.3rem;
  }
  table, th, td {
    font-size: 0.85rem;
  }
}
</style> 