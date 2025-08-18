<template>
  <div class="not-found">
    <div class="not-found-content">
      <h1>404</h1>
      <h2>Página não encontrada</h2>
      <p>A página que você está procurando não existe ou foi movida.</p>
      <router-link to="/login" class="back-btn">Voltar para o Login</router-link>
    </div>
    <Footer :full-width="true" />
  </div>
</template>

<script setup>
import Footer from '../components/Footer.vue'
</script>

<style scoped>
.not-found {
  min-height: 100vh;
  background: linear-gradient(135deg, #CFE3C6 0%, #F5F6FA 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem 2rem 0 2rem;
  position: relative;
  box-sizing: border-box;
}

.not-found-content {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 4px 24px #17635a22;
  padding: 3rem 2rem;
  text-align: center;
  max-width: 400px;
  width: 100%;
  box-sizing: border-box;
  margin: auto 0 2rem 0;
  flex-shrink: 0;
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

@media (max-width: 768px) {
  .not-found {
    padding: 1.5rem 1rem 0 1rem;
    padding-top: 3rem;
  }

  .not-found-content {
    padding: 2.5rem 1.5rem;
    max-width: 90%;
    margin: auto 0 1.5rem 0;
  }

  .not-found-content h1 {
    font-size: 3.5rem;
  }

  .not-found-content h2 {
    font-size: 1.3rem;
  }
}

@media (max-width: 500px) {
  .not-found {
    padding: 1rem 0.8rem 0 0.8rem;
    padding-top: 2.5rem;
  }

  .not-found-content {
    padding: 2rem 1rem;
    max-width: 95%;
    border-radius: 12px;
    margin: auto 0 1.2rem 0;
  }

  .not-found-content h1 {
    font-size: 3rem;
    margin-bottom: 0.8rem;
  }

  .not-found-content h2 {
    font-size: 1.2rem;
    margin-bottom: 0.8rem;
  }

  .not-found-content p {
    margin-bottom: 1.5rem;
    font-size: 0.95rem;
  }

  .back-btn {
    padding: 0.7rem 1.2rem;
    font-size: 0.95rem;
  }
}

@media (max-width: 360px) {
  .not-found {
    padding: 0.8rem 0.5rem 0 0.5rem;
    padding-top: 2rem;
  }

  .not-found-content {
    padding: 1.8rem 0.8rem;
    max-width: 98%;
    border-radius: 10px;
    margin: auto 0 1rem 0;
  }

  .not-found-content h1 {
    font-size: 2.5rem;
    margin-bottom: 0.6rem;
  }

  .not-found-content h2 {
    font-size: 1.1rem;
    margin-bottom: 0.6rem;
  }

  .not-found-content p {
    margin-bottom: 1.2rem;
    font-size: 0.9rem;
    line-height: 1.4;
  }

  .back-btn {
    padding: 0.6rem 1rem;
    font-size: 0.9rem;
  }
}

@media (max-height: 600px) and (orientation: landscape) {
  .not-found {
    padding: 1rem 2rem 0 2rem;
    padding-top: 1.5rem;
  }

  .not-found-content {
    padding: 2rem 1.5rem;
    max-width: 80%;
    margin: auto 0 1rem 0;
  }

  .not-found-content h1 {
    font-size: 3rem;
    margin-bottom: 0.5rem;
  }

  .not-found-content h2 {
    font-size: 1.2rem;
    margin-bottom: 0.5rem;
  }

  .not-found-content p {
    margin-bottom: 1rem;
  }
}
</style>
