<template>
  <div class="evaluator-dashboard">
    <h2>Trabalhos Atribuídos</h2>
    <div v-if="loadingWorks" class="loading">Carregando trabalhos...</div>
    <div v-else>
      <div v-if="works.length" class="works-container">
        <div class="works-grid">
          <div v-for="work in works" :key="work.id" class="work-card">
            <div class="work-title">{{ work.title }}</div>
            <div class="work-authors">{{ work.authors }}</div>
            <div class="work-action">
              <router-link v-if="!isWorkEvaluated(work.id)" :to="`/evaluate/${work.id}`" class="eval-btn">Avaliar</router-link>
              <span v-else class="evaluated-text">Avaliado</span>
            </div>
          </div>
        </div>
      </div>
      <div v-else class="empty">Nenhum trabalho atribuído.</div>
      <div v-if="worksError" class="error">{{ worksError }}</div>
    </div>

    <h2 class="section-title">Minhas Avaliações</h2>
    <div v-if="loadingEvals" class="loading">Carregando avaliações...</div>
    <div v-else>
      <div v-if="evaluations.length" class="evaluations-container">
        <div class="evaluations-grid">
          <div v-for="evaluation in evaluations" :key="evaluation.id" class="evaluation-card">
            <div class="eval-work-title">{{ evaluation.work_title }}</div>
            <div class="eval-method">{{ getMethodLabel(evaluation.method) }}</div>
          </div>
        </div>
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
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(23, 99, 90, 0.12);
  padding: 2.5rem;
  margin: 2rem auto;
  width: 85%;
  max-width: 1100px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  min-height: 85vh;
  position: relative;
  border: 1px solid rgba(23, 99, 90, 0.08);
}

h2 {
  color: #17635A;
  font-size: 1.8rem;
  margin-bottom: 1.5rem;
  font-weight: 800;
  text-align: center;
  flex-shrink: 0;
  letter-spacing: 0.5px;
}

.section-title {
  margin-top: 2.5rem;
  flex-shrink: 0;
}

.works-container,
.evaluations-container {
  margin-bottom: 1.5rem;
  flex: 1;
}

.works-grid,
.evaluations-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 1.5rem;
  margin-bottom: 1rem;
}

.work-card,
.evaluation-card {
  background: #fff;
  border: 1px solid #E8F5E8;
  border-radius: 16px;
  padding: 1.8rem;
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  min-height: 120px;
  box-shadow: 0 4px 20px rgba(23, 99, 90, 0.08);
  transition: all 0.3s ease;
  border-left: 4px solid #4CB050;
}

.evaluation-card {
  justify-content: flex-start;
  min-height: 100px;
}

.work-card:hover,
.evaluation-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(23, 99, 90, 0.12);
  border-color: #CFE3C6;
}

.work-title,
.eval-work-title {
  color: #17635A;
  font-weight: 700;
  font-size: 1.1rem;
  margin-bottom: 0.8rem;
  line-height: 1.4;
  word-wrap: break-word;
  position: relative;
  z-index: 1;
}

.work-authors {
  color: #555;
  font-size: 0.95rem;
  margin-bottom: 1rem;
  line-height: 1.3;
  word-wrap: break-word;
  font-weight: 500;
}

.eval-method {
  color: #4CB050;
  font-weight: 600;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  background: rgba(76, 176, 80, 0.1);
  padding: 0.3rem 0.6rem;
  border-radius: 6px;
  display: inline-block;
  width: fit-content;
}

.eval-criteria {
  color: #555;
  font-size: 0.9rem;
  line-height: 1.4;
  word-wrap: break-word;
  background: #FAFFFA;
  padding: 0.8rem;
  border-radius: 8px;
  border-left: 3px solid #CFE3C6;
}

.work-action {
  margin-top: 1rem;
  text-align: center;
}

.eval-btn {
  background: #4CB050;
  color: #fff;
  border: none;
  border-radius: 10px;
  padding: 0.7rem 1.4rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s ease;
  display: inline-block;
  font-size: 0.9rem;
  min-width: 80px;
  margin-top: auto;
  align-self: center;
  text-align: center;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(76, 176, 80, 0.2);
}

.eval-btn:hover {
  background: #17635A;
  box-shadow: 0 4px 12px rgba(76, 176, 80, 0.3);
}

.evaluated-text {
  color: #4CB050;
  font-weight: 600;
  font-size: 0.9rem;
  text-align: center;
  padding: 0.6rem 1.2rem;
  background: rgba(76, 176, 80, 0.1);
  border-radius: 8px;
  border: 1px solid rgba(76, 176, 80, 0.2);
}

.loading {
  color: #17635A;
  font-weight: 600;
  margin: 1rem 0;
  text-align: center;
  padding: 1rem;
  background: rgba(23, 99, 90, 0.05);
  border-radius: 8px;
  border: 1px solid rgba(23, 99, 90, 0.1);
}

.error {
  color: #b00020;
  margin-top: 1rem;
  font-weight: 600;
  padding: 1rem;
  background: rgba(176, 0, 32, 0.05);
  border-radius: 8px;
  border: 1px solid rgba(176, 0, 32, 0.1);
  text-align: center;
}

.empty {
  color: #888;
  margin: 1.5rem 0;
  font-style: italic;
  text-align: center;
  padding: 2rem;
  background: rgba(136, 136, 136, 0.05);
  border-radius: 8px;
  border: 1px solid rgba(136, 136, 136, 0.1);
}

@media (max-width: 1024px) {
  .evaluator-dashboard {
    padding: 2rem;
    margin: 1.5rem auto;
    width: 90%;
    min-height: 80vh;
  }

  h2 {
    font-size: 1.6rem;
    margin-bottom: 1.3rem;
  }

  .section-title {
    margin-top: 2rem;
  }

  .works-container,
  .evaluations-container {
    margin-bottom: 1.3rem;
  }

  .works-grid,
  .evaluations-grid {
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.3rem;
  }

  .work-card,
  .evaluation-card {
    padding: 1.3rem;
  }

  .work-title,
  .eval-work-title {
    font-size: 1rem;
    margin-bottom: 0.7rem;
  }

  .work-authors {
    font-size: 0.9rem;
    margin-bottom: 0.8rem;
  }

  .eval-method {
    font-size: 0.85rem;
  }

  .eval-criteria {
    font-size: 0.85rem;
  }
}

@media (max-width: 768px) {
  .evaluator-dashboard {
    padding: 1.5rem;
    margin: 1rem auto;
    border-radius: 14px;
    min-height: 75vh;
    width: 92%;
  }

  h2 {
    font-size: 1.4rem;
    margin-bottom: 1.2rem;
  }

  .section-title {
    margin-top: 1.8rem;
  }

  .works-container,
  .evaluations-container {
    margin-bottom: 1.2rem;
  }

  .works-grid,
  .evaluations-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .work-card,
  .evaluation-card {
    padding: 1.2rem;
  }

  .work-title,
  .eval-work-title {
    font-size: 1rem;
    margin-bottom: 0.6rem;
  }

  .work-authors {
    font-size: 0.9rem;
    margin-bottom: 0.7rem;
  }

  .eval-method {
    font-size: 0.8rem;
  }

  .eval-criteria {
    font-size: 0.8rem;
  }

  .eval-btn {
    padding: 0.6rem 1.2rem;
    font-size: 0.9rem;
    min-width: 80px;
  }

  .evaluated-text {
    padding: 0.6rem 1.2rem;
    font-size: 0.9rem;
  }
}

@media (max-width: 480px) {
  .evaluator-dashboard {
    padding: 1rem;
    margin: 1rem auto;
    min-height: 70vh;
    width: 94%;
  }

  h2 {
    font-size: 1.3rem;
    margin-bottom: 1rem;
  }

  .section-title {
    margin-top: 1.5rem;
  }

  .works-container,
  .evaluations-container {
    margin-bottom: 1rem;
  }

  .works-grid,
  .evaluations-grid {
    gap: 0.8rem;
  }

  .work-card,
  .evaluation-card {
    padding: 1rem;
    border-radius: 10px;
  }

  .work-title,
  .eval-work-title {
    font-size: 0.95rem;
    margin-bottom: 0.5rem;
  }

  .work-authors {
    font-size: 0.85rem;
    margin-bottom: 0.6rem;
  }

  .eval-method {
    font-size: 0.75rem;
  }

  .eval-criteria {
    font-size: 0.75rem;
  }

  .eval-btn {
    padding: 0.6rem 1.2rem;
    font-size: 0.9rem;
    min-width: 80px;
  }

  .evaluated-text {
    padding: 0.6rem 1.2rem;
    font-size: 0.9rem;
  }

  .loading,
  .error,
  .empty {
    font-size: 0.9rem;
    padding: 0.8rem;
  }
}

@media (max-width: 360px) {
  .evaluator-dashboard {
    padding: 0.8rem;
    margin: 0.8rem auto;
    min-height: 65vh;
    width: 96%;
  }

  h2 {
    font-size: 1.2rem;
    margin-bottom: 0.8rem;
  }

  .section-title {
    margin-top: 1.3rem;
  }

  .works-container,
  .evaluations-container {
    margin-bottom: 0.8rem;
  }

  .works-grid,
  .evaluations-grid {
    gap: 0.6rem;
  }

  .work-card,
  .evaluation-card {
    padding: 0.8rem;
    border-radius: 8px;
  }

  .work-title,
  .eval-work-title {
    font-size: 0.9rem;
    margin-bottom: 0.4rem;
  }

  .work-authors {
    font-size: 0.8rem;
    margin-bottom: 0.5rem;
  }

  .eval-method {
    font-size: 0.7rem;
  }

  .eval-criteria {
    font-size: 0.7rem;
  }

  .eval-btn {
    padding: 0.6rem 1.2rem;
    font-size: 0.9rem;
    min-width: 80px;
  }

  .evaluated-text {
    padding: 0.6rem 1.2rem;
    font-size: 0.9rem;
  }

  .loading,
  .error,
  .empty {
    font-size: 0.85rem;
    padding: 0.7rem;
  }
}
</style>
