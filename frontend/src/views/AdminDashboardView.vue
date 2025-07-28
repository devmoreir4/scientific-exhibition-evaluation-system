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
        <div class="card-title">Pôsteres/Banners</div>
        <div class="card-value">{{ posterCount }}</div>
        <span class="card-subtitle">de {{ works.length }} trabalhos</span>
      </div>
      <div class="card">
        <div class="card-title">Apresentações Orais</div>
        <div class="card-value">{{ oralCount }}</div>
        <span class="card-subtitle">de {{ works.length }} trabalhos</span>
      </div>
      <div class="card">
        <div class="card-title">Fichas Manuais</div>
        <div class="card-value">-</div>
        <router-link to="/admin/sheets">Ver Fichas</router-link>
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

const posterCount = computed(() => {
  return works.value.filter(w => w.type === 'poster_banner').length
})

const oralCount = computed(() => {
  return works.value.filter(w => w.type === 'oral_presentation').length
})

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
  margin-top: 1rem;
}
h2 {
  color: #17635A;
  font-size: 1.5rem;
  margin-bottom: 2rem;
}
.cards {
  display: flex;
  gap: 2rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}
.card {
  background: #CFE3C6;
  border-radius: 10px;
  box-shadow: 0 1px 6px #17635a11;
  padding: 1.5rem 2rem;
  min-width: 180px;
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
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
.card-subtitle {
  color: #17635A;
  font-size: 0.9rem;
  font-weight: 600;
  opacity: 0.8;
}
.card a {
  background: #17635A;
  color: #fff;
  border-radius: 6px;
  padding: 0.3rem 1rem;
  text-decoration: none;
  font-weight: 700;
  transition: background 0.2s;
}
.card a:hover {
  background: #4CB050;
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
@media (max-width: 900px) {
  .cards {
    flex-direction: column;
    gap: 1.2rem;
  }
  .card {
    min-width: 0;
    width: 100%;
  }
}
</style> 