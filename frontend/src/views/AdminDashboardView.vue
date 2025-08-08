<template>
  <div class="admin-dashboard">
    <h2>Painel do Administrador</h2>
    <div class="cards">
      <div class="card">
        <div class="card-title">Avaliadores</div>
        <div class="card-value">{{ users.length }}</div>
        <router-link to="/admin/users">Ver Avaliadores</router-link>
      </div>
      <div class="card">
        <div class="card-title">Trabalhos</div>
        <div class="card-value">{{ works.length }}</div>
        <router-link to="/admin/works">Ver Trabalhos</router-link>
      </div>
      <div class="card">
        <div class="card-title">Ferramentas</div>
        <div class="card-value">-</div>
        <router-link to="/admin/sheets">Ver Ferramentas</router-link>
      </div>
      <div class="card">
        <div class="card-title">Distribuições</div>
        <div class="card-value">-</div>
        <router-link to="/admin/distributions">Ver Distribuições</router-link>
      </div>
      <div class="card">
        <div class="card-title">Monitoramento</div>
        <div class="card-value">-</div>
        <router-link to="/admin/monitoring">Ver Progresso</router-link>
      </div>
      <div class="card">
        <div class="card-title">Pódio</div>
        <div class="card-value">-</div>
        <router-link to="/admin/podium">Ver Pódio</router-link>
      </div>
    </div>
    <div v-if="loading" class="loading">Carregando dados...</div>
    <div v-if="error" class="error">{{ error }}</div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../axios'

const users = ref([])
const works = ref([])
const loading = ref(true)
const error = ref('')

async function fetchData() {
  loading.value = true
  error.value = ''
  try {
    const [usersRes, worksRes] = await Promise.all([
      api.get('/admin/users'),
      api.get('/admin/works')
    ])
    users.value = usersRes.data.users || []
    works.value = worksRes.data.works || []
  } catch (e) {
    error.value = e.response?.data?.msg || 'Erro ao carregar dados.'
  } finally {
    loading.value = false
  }
}

onMounted(fetchData)
</script>

<style scoped>
.admin-dashboard {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px #17635a22;
  padding: 2rem;
  margin: 1rem;
}

h2 {
  color: #17635A;
  font-size: 1.5rem;
  margin-bottom: 2rem;
  text-align: center;
  font-weight: 700;
}

.cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.card {
  background: #CFE3C6;
  border-radius: 10px;
  box-shadow: 0 1px 6px #17635a11;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  transition: transform 0.2s, box-shadow 0.2s;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px #17635a22;
}

.card-title {
  color: #17635A;
  font-weight: 700;
  font-size: 1.1rem;
  margin-bottom: 0.7rem;
}

.card-value {
  color: #4CB050;
  font-size: 2.2rem;
  font-weight: 900;
  margin-bottom: 0.7rem;
}

.card a {
  background: #17635A;
  color: #fff;
  border-radius: 6px;
  padding: 0.4rem 1rem;
  text-decoration: none;
  font-weight: 700;
  font-size: 0.9rem;
  transition: background 0.2s;
  width: 100%;
  text-align: center;
  box-sizing: border-box;
}

.card a:hover {
  background: #4CB050;
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
  padding: 0.8rem;
  background: rgba(176, 0, 32, 0.1);
  border-radius: 6px;
  text-align: center;
}
</style>
