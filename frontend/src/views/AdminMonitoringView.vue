<template>
  <div class="admin-monitoring">
    <h2>Monitoramento de Avaliações</h2>

    <div class="stats-cards">
      <div class="stat-card">
        <div class="stat-title">Total de Trabalhos</div>
        <div class="stat-value">{{ overallStats.total_works || 0 }}</div>
      </div>
      <div class="stat-card">
        <div class="stat-title">Avaliações Realizadas</div>
        <div class="stat-value">{{ overallStats.total_evaluations || 0 }}</div>
      </div>
      <div class="stat-card">
        <div class="stat-title">Avaliações Pendentes</div>
        <div class="stat-value">{{ (overallStats.total_expected_evaluations || 0) - (overallStats.total_evaluations || 0) }}</div>
      </div>
      <div class="stat-card progress-card">
        <div class="stat-title">Progresso Geral</div>
        <div class="stat-value">{{ overallStats.overall_progress || 0 }}%</div>
        <div class="progress-bar">
          <div class="progress-fill" :style="{ width: (overallStats.overall_progress || 0) + '%' }"></div>
        </div>
      </div>
    </div>

    <div class="works-progress-section">
      <h3>Progresso por Trabalho</h3>
      <div v-if="loading" class="loading">Carregando dados de monitoramento...</div>
      <div v-else>
        <div v-if="worksProgress.length === 0" class="empty">
          <span v-if="!isDistributed">
            Nenhum trabalho encontrado. Realize a distribuição primeiro.
          </span>
          <span v-else>
            Nenhum trabalho distribuído encontrado.
          </span>
        </div>
        <div v-else class="works-list">
          <div v-for="work in worksProgress" :key="work.work_id" class="work-item">
            <div class="work-header">
              <h4>{{ work.work_title }}</h4>
              <div class="work-progress-info">
                <span class="progress-text">{{ work.progress_percentage }}%</span>
                <span class="evaluations-text">{{ work.completed_evaluations }}/{{ work.total_evaluators }} avaliações</span>
              </div>
            </div>
            <div class="work-details">
              <span class="area-info">{{ work.work_area }} | {{ work.work_subarea }}</span>
            </div>
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: work.progress_percentage + '%' }"></div>
            </div>
            <div class="status-info">
              <span v-if="!isDistributed" class="not-distributed">
                Trabalhos ainda não distribuídos
              </span>
              <span v-else-if="work.pending_evaluations > 0" class="pending">
                {{ work.pending_evaluations }} avaliação(ões) pendente(s)
                <div class="pending-evaluators">
                  <span class="pending-label">Avaliadores pendentes:</span>
                  <span v-for="evaluator in work.pending_evaluators" :key="evaluator.id" class="evaluator-tag">
                    {{ evaluator.name }}
                  </span>
                </div>
              </span>
              <span v-else class="completed">
                Todas as avaliações concluídas
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="refresh-section">
      <button @click="fetchMonitoringData" :disabled="loading" class="refresh-btn">
        {{ loading ? 'Atualizando...' : 'Atualizar Dados' }}
      </button>
    </div>

    <div v-if="error" class="error">{{ error }}</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../axios'

const overallStats = ref({})
const worksProgress = ref([])
const loading = ref(true)
const error = ref('')
const isDistributed = ref(false)

async function fetchMonitoringData() {
  loading.value = true
  error.value = ''
  try {
    const distributionResponse = await api.get('/admin/works/distribution-status')
    isDistributed.value = distributionResponse.data.distributed

    const response = await api.get('/admin/works/evaluation-progress')
    overallStats.value = response.data.overall_stats
    worksProgress.value = response.data.works_progress
  } catch (e) {
    console.error('Erro ao buscar dados de monitoramento:', e)
    error.value = e.response?.data?.msg || 'Erro ao carregar dados de monitoramento.'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchMonitoringData()
})
</script>

<style scoped>
.admin-monitoring {
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

h3 {
  color: #17635A;
  font-size: 1.2rem;
  margin-bottom: 1rem;
}

.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: #CFE3C6;
  border-radius: 10px;
  padding: 1.5rem;
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

.progress-card {
  background: linear-gradient(135deg, #CFE3C6 0%, #E8F5E8 100%);
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: #e0e0e0;
  border-radius: 4px;
  margin-top: 0.5rem;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: #4CB050;
  transition: width 0.3s ease;
}

.works-progress-section {
  margin-bottom: 2rem;
}

.works-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.work-item {
  background: #F5F6FA;
  border-radius: 10px;
  padding: 1.5rem;
  border: 1px solid #e0e0e0;
}

.work-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.5rem;
}

.work-header h4 {
  color: #17635A;
  font-size: 1.1rem;
  margin: 0;
  flex: 1;
}

.work-progress-info {
  text-align: right;
  margin-left: 1rem;
}

.progress-text {
  display: block;
  font-weight: 700;
  color: #4CB050;
  font-size: 1.1rem;
}

.evaluations-text {
  display: block;
  color: #666;
  font-size: 0.9rem;
}

.work-details {
  margin-bottom: 1rem;
}

.area-info {
  color: #666;
  font-size: 0.9rem;
}

.status-info {
  margin-top: 0.5rem;
  font-size: 0.9rem;
}

.pending {
  color: #666;
}

.pending-evaluators {
  margin-top: 0.5rem;
  display: flex;
  flex-wrap: wrap;
  gap: 0.8rem;
  align-items: center;
}

.pending-label {
  font-size: 0.8rem;
  color: #888;
  font-weight: 600;
  margin-right: 0.5rem;
}

.evaluator-tag {
  color: #17635A;
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.2rem 0.6rem;
  border: 1px solid #17635A;
  border-radius: 12px;
  background: #F5F6FA;
}

.completed {
  color: #4CAF50;
}

.not-distributed {
  color: #666;
}

.refresh-section {
  text-align: center;
  margin-top: 1rem;
}

.refresh-btn {
  background: #4CB050;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 0.8rem 1.5rem;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.2s;
}

.refresh-btn:hover {
  background: #17635A;
}

.refresh-btn:disabled {
  background: #CFE3C6;
  color: #17635A;
  cursor: not-allowed;
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
