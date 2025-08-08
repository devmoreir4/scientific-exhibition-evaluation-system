<template>
  <div class="admin-distributions">
    <h2>Distribuições de Trabalhos</h2>

    <div class="stats-cards">
      <div class="stat-card">
        <div class="stat-title">Total de Trabalhos</div>
        <div class="stat-value">{{ distributions.length }}</div>
      </div>
      <div class="stat-card">
        <div class="stat-title">Trabalhos Distribuídos</div>
        <div class="stat-value">{{ distributedWorks }}</div>
      </div>
      <div class="stat-card">
        <div class="stat-title">Trabalhos Não Distribuídos</div>
        <div class="stat-value">{{ nonDistributedWorks }}</div>
      </div>
    </div>

    <div v-if="loading" class="loading">Carregando distribuições...</div>
    <div v-else>
      <div v-if="distributions.length === 0" class="empty">
        Nenhum trabalho encontrado. Importe trabalhos primeiro.
      </div>
      <div v-else class="distributions-list">
        <div v-for="distribution in distributions" :key="distribution.work_id" class="distribution-item">
          <div class="work-info">
            <h3>{{ distribution.work_title }}</h3>
            <div class="work-details">
              <span><strong>Autores:</strong> {{ distribution.work_authors }}</span>
              <span><strong>Orientador:</strong> {{ distribution.work_advisor }}</span>
              <span><strong>Tipo:</strong> {{ getTypeLabel(distribution.work_type) }}</span>
              <span><strong>Área:</strong> {{ distribution.work_area }}</span>
              <span><strong>Subárea:</strong> {{ distribution.work_subarea }}</span>
            </div>
          </div>

          <div class="evaluators-section">
            <h4>Avaliadores Atribuídos ({{ distribution.evaluators_count }})</h4>
            <div v-if="distribution.evaluators.length === 0" class="no-evaluators">
              <span class="warning">Nenhum avaliador atribuído</span>
            </div>
            <div v-else class="evaluators-list">
              <div v-for="evaluator in distribution.evaluators" :key="evaluator.id" class="evaluator-item">
                <div class="evaluator-info">
                  <span class="evaluator-name">{{ evaluator.name }}</span>
                  <span class="evaluator-details">
                    SIAPE/CPF: {{ evaluator.siape_or_cpf }} |
                    Área: {{ evaluator.area }} |
                    Subáreas: {{ evaluator.subareas || 'Não informadas' }} |
                    Carga: {{ evaluator.workload }}
                  </span>
                </div>
                <div class="evaluator-type" :class="getEvaluatorTypeClass(evaluator.area)">
                  {{ getEvaluatorTypeLabel(evaluator.area) }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>


      <Pagination
        v-if="pagination && pagination.total > 0"
        :pagination="pagination"
        @page-change="onPageChange"
        @per-page-change="onPerPageChange"
      />

      <div v-if="error" class="error">{{ error }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../axios'
import Pagination from '../components/Pagination.vue'

const distributions = ref([])
const loading = ref(true)
const error = ref('')
const pagination = ref(null)
const currentPage = ref(1)
const currentPerPage = ref(20)

const distributedWorks = computed(() => {
  return distributions.value.filter(d => d.evaluators_count > 0).length
})

const nonDistributedWorks = computed(() => {
  return distributions.value.filter(d => d.evaluators_count === 0).length
})

function getTypeLabel(type) {
  const types = {
    'poster_banner': 'Pôster/Banner',
    'oral_presentation': 'Apresentação Oral'
  }
  return types[type] || type
}

function getEvaluatorTypeLabel(area) {
  return area.toLowerCase().includes('pedag') ? 'Pedagógico' : 'Técnico'
}

function getEvaluatorTypeClass(area) {
  return area.toLowerCase().includes('pedag') ? 'pedagogico' : 'tecnico'
}

async function fetchDistributions() {
  loading.value = true
  error.value = ''
  try {
    const params = new URLSearchParams({
      page: currentPage.value.toString(),
      per_page: currentPerPage.value.toString()
    })

    const response = await api.get(`/admin/works/distributions?${params}`)
    distributions.value = response.data.distributions || []
    pagination.value = response.data.pagination
  } catch (e) {
    console.error('Erro ao buscar distribuições:', e, e.response)
    error.value = e.response?.data?.msg || 'Erro ao carregar distribuições.'
  } finally {
    loading.value = false
  }
}

function onPageChange(page) {
  currentPage.value = page
  fetchDistributions()
}

function onPerPageChange(perPage) {
  currentPerPage.value = perPage
  currentPage.value = 1
  fetchDistributions()
}

onMounted(fetchDistributions)
</script>

<style scoped>
.admin-distributions {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px #17635a22;
  padding: 2rem;
}

h2 {
  color: #17635A;
  font-size: 1.5rem;
  margin-bottom: 2rem;
  text-align: center;
}

.stats-cards {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.stat-card {
  background: #CFE3C6;
  border-radius: 10px;
  padding: 1.5rem;
  min-width: 180px;
  flex: 1;
  text-align: center;
  box-shadow: 0 1px 6px #17635a11;
}

.stat-title {
  color: #17635A;
  font-weight: 700;
  font-size: 1rem;
  margin-bottom: 0.5rem;
}

.stat-value {
  color: #4CB050;
  font-size: 2rem;
  font-weight: 900;
}

.distributions-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.distribution-item {
  border: 1px solid #CFE3C6;
  border-radius: 10px;
  padding: 1.5rem;
  background: #F5F6FA;
}

.work-info h3 {
  color: #17635A;
  font-size: 1.2rem;
  margin-bottom: 1rem;
  font-weight: 700;
}

.work-details {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
  font-size: 0.95rem;
  color: #666;
}

.work-details span {
  display: block;
}

.evaluators-section h4 {
  color: #17635A;
  font-size: 1.1rem;
  margin-bottom: 1rem;
  font-weight: 700;
}

.no-evaluators {
  text-align: center;
  padding: 1rem;
  background: #fff0f0;
  border-radius: 8px;
  border: 1px solid #ffcdd2;
}

.warning {
  color: #d32f2f;
  font-weight: 600;
}

.evaluators-list {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.evaluator-item {
  background: #fff;
  border-radius: 8px;
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border: 1px solid #e0e0e0;
  gap: 1.5rem;
}

.evaluator-info {
  flex: 1;
}

.evaluator-name {
  display: block;
  font-weight: 700;
  color: #17635A;
  margin-bottom: 0.3rem;
}

.evaluator-details {
  font-size: 0.9rem;
  color: #666;
}

.evaluator-type {
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  min-width: 100px;
  text-align: center;
  flex-shrink: 0;
}

.evaluator-type.pedagogico {
  background: #e3f2fd;
  color: #1976d2;
}

.evaluator-type.tecnico {
  background: #f3e5f5;
  color: #7b1fa2;
}

.loading {
  color: #17635A;
  font-weight: 600;
  margin: 1rem 0;
  text-align: center;
}

.error {
  color: #b00020;
  margin-top: 1rem;
  font-weight: 600;
  text-align: center;
}

.empty {
  color: #888;
  margin: 2rem 0;
  font-style: italic;
  text-align: center;
}
</style>
