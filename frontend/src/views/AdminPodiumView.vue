<template>
  <div class="admin-podium">
    <h2>Pódio dos Trabalhos por Área</h2>

    <div v-if="loading" class="loading">Carregando pódio...</div>
    <div v-else>
      <div v-if="Object.keys(podiumData).length === 0" class="empty">
        Nenhum trabalho avaliado encontrado. Aguarde as avaliações serem concluídas.
      </div>
      <div v-else class="podium-sections">
        <div v-for="(areaData, areaKey) in podiumData" :key="areaKey" class="area-podium">
          <div class="area-header">
            <h3>{{ areaData.area_name }}</h3>
            <div class="area-stats">
              <span>{{ areaData.evaluated_works }} de {{ areaData.total_works }} trabalhos avaliados</span>
            </div>
          </div>

          <div v-if="areaData.podium.length === 0" class="no-podium">
            Nenhum trabalho desta área foi avaliado ainda.
          </div>
          <div v-else class="podium-positions">
            <!-- 1º Lugar -->
            <div v-if="areaData.podium[0]" class="podium-item first-place">
              <div class="medal">🥇</div>
              <div class="position">1º Lugar</div>
              <div class="work-info">
                <h4>{{ areaData.podium[0].work_title }}</h4>
                <div class="work-details">
                  <span><strong>Autores:</strong> {{ areaData.podium[0].work_authors }}</span>
                  <span><strong>Orientador:</strong> {{ areaData.podium[0].work_advisor }}</span>
                  <span><strong>Subárea:</strong> {{ areaData.podium[0].work_subarea }}</span>
                  <span><strong>Tipo:</strong> {{ getTypeLabel(areaData.podium[0].work_type) }}</span>
                </div>
              </div>
              <div class="score-info">
                <div class="average-score">{{ areaData.podium[0].average_score }}</div>
                <div class="score-label">Média</div>
                <div class="evaluations-count">{{ areaData.podium[0].evaluations_count }} avaliações</div>
              </div>
            </div>

            <!-- 2º Lugar -->
            <div v-if="areaData.podium[1]" class="podium-item second-place">
              <div class="medal">🥈</div>
              <div class="position">2º Lugar</div>
              <div class="work-info">
                <h4>{{ areaData.podium[1].work_title }}</h4>
                <div class="work-details">
                  <span><strong>Autores:</strong> {{ areaData.podium[1].work_authors }}</span>
                  <span><strong>Orientador:</strong> {{ areaData.podium[1].work_advisor }}</span>
                  <span><strong>Subárea:</strong> {{ areaData.podium[1].work_subarea }}</span>
                  <span><strong>Tipo:</strong> {{ getTypeLabel(areaData.podium[1].work_type) }}</span>
                </div>
              </div>
              <div class="score-info">
                <div class="average-score">{{ areaData.podium[1].average_score }}</div>
                <div class="score-label">Média</div>
                <div class="evaluations-count">{{ areaData.podium[1].evaluations_count }} avaliações</div>
              </div>
            </div>

            <!-- 3º Lugar -->
            <div v-if="areaData.podium[2]" class="podium-item third-place">
              <div class="medal">🥉</div>
              <div class="position">3º Lugar</div>
              <div class="work-info">
                <h4>{{ areaData.podium[2].work_title }}</h4>
                <div class="work-details">
                  <span><strong>Autores:</strong> {{ areaData.podium[2].work_authors }}</span>
                  <span><strong>Orientador:</strong> {{ areaData.podium[2].work_advisor }}</span>
                  <span><strong>Subárea:</strong> {{ areaData.podium[2].work_subarea }}</span>
                  <span><strong>Tipo:</strong> {{ getTypeLabel(areaData.podium[2].work_type) }}</span>
                </div>
              </div>
              <div class="score-info">
                <div class="average-score">{{ areaData.podium[2].average_score }}</div>
                <div class="score-label">Média</div>
                <div class="evaluations-count">{{ areaData.podium[2].evaluations_count }} avaliações</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Botão de Atualização -->
    <div class="refresh-section">
      <button @click="fetchPodiumData" :disabled="loading" class="refresh-btn">
        {{ loading ? 'Atualizando...' : 'Atualizar Pódio' }}
      </button>
    </div>

    <div v-if="error" class="error">{{ error }}</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../axios'

const podiumData = ref({})
const loading = ref(true)
const error = ref('')

function getTypeLabel(type) {
  const types = {
    'poster_banner': 'Pôster/Banner',
    'oral_presentation': 'Apresentação Oral'
  }
  return types[type] || type
}

async function fetchPodiumData() {
  loading.value = true
  error.value = ''
  try {
    const response = await api.get('/admin/works/podium')
    podiumData.value = response.data.podium_data
  } catch (e) {
    console.error('Erro ao buscar dados do pódio:', e)
    error.value = e.response?.data?.msg || 'Erro ao carregar pódio.'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchPodiumData()
})
</script>

<style scoped>
.admin-podium {
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

.podium-sections {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.area-podium {
  background: #F5F6FA;
  border-radius: 12px;
  padding: 1.5rem;
  border: 1px solid #e0e0e0;
}

.area-header {
  text-align: center;
  margin-bottom: 1.5rem;
}

.area-header h3 {
  color: #17635A;
  font-size: 1.3rem;
  margin-bottom: 0.5rem;
  font-weight: 700;
}

.area-stats {
  color: #666;
  font-size: 0.9rem;
}

.no-podium {
  text-align: center;
  color: #888;
  font-style: italic;
  padding: 2rem;
}

.podium-positions {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.podium-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  background: #fff;
  border-radius: 10px;
  padding: 1.5rem;
  border: 2px solid #e0e0e0;
  transition: transform 0.2s;
}

.podium-item:hover {
  transform: translateY(-2px);
}

.first-place {
  border-color: #FFD700;
  background: linear-gradient(135deg, #fff 0%, #FFF8E1 100%);
}

.second-place {
  border-color: #C0C0C0;
  background: linear-gradient(135deg, #fff 0%, #F5F5F5 100%);
}

.third-place {
  border-color: #CD7F32;
  background: linear-gradient(135deg, #fff 0%, #FFF3E0 100%);
}

.medal {
  font-size: 2rem;
  min-width: 60px;
  text-align: center;
}

.position {
  font-weight: 700;
  font-size: 1.1rem;
  min-width: 80px;
  text-align: center;
}

.first-place .position {
  color: #DAA520;
}

.second-place .position {
  color: #808080;
}

.third-place .position {
  color: #CD7F32;
}

.work-info {
  flex: 1;
}

.work-info h4 {
  color: #17635A;
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
  font-weight: 700;
}

.work-details {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
  font-size: 0.9rem;
  color: #666;
}

.work-details span {
  display: block;
}

.score-info {
  text-align: center;
  min-width: 100px;
}

.average-score {
  font-size: 2rem;
  font-weight: 900;
  color: #4CB050;
  line-height: 1;
}

.score-label {
  font-size: 0.8rem;
  color: #666;
  margin-bottom: 0.3rem;
}

.evaluations-count {
  font-size: 0.8rem;
  color: #888;
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

@media (max-width: 900px) {
  .podium-item {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }

  .medal, .position {
    min-width: auto;
  }

  .score-info {
    min-width: auto;
  }
}

@media (max-width: 600px) {
  .admin-podium {
    padding: 1rem 0.3rem;
  }

  .area-podium {
    padding: 1rem;
  }

  .podium-item {
    padding: 1rem;
  }

  .work-details {
    font-size: 0.85rem;
  }
}
</style>
