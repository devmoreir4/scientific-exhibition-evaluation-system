<template>
  <div class="not-found">
    <div class="not-found-content">
      <h1>404</h1>
      <h2>Página não encontrada</h2>
      <p>A página que você está procurando não existe ou foi movida.</p>
      <router-link to="/login" class="back-btn">Voltar para o Login</router-link>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.not-found {
  min-height: 100vh;
  background: linear-gradient(135deg, #CFE3C6 0%, #F5F6FA 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}
.not-found-content {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 4px 24px #17635a22;
  padding: 3rem 2rem;
  text-align: center;
  max-width: 400px;
  width: 100%;
}
.not-found-content h1 {
  color: #17635A;
  font-size: 4rem;
  font-weight: 900;
  margin-bottom: 1rem;
  letter-spacing: 2px;
}
.not-found-content h2 {
  color: #4CB050;
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
}
.not-found-content p {
  color: #666;
  margin-bottom: 2rem;
  line-height: 1.5;
}
.back-btn {
  background: #17635A;
  color: #fff;
  text-decoration: none;
  padding: 0.8rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  transition: background 0.2s;
  display: inline-block;
}
.back-btn:hover {
  background: #4CB050;
}
</style> 