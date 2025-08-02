<template>
  <footer :class="['standalone-footer', { 'full-width': fullWidth }]">
    <div class="footer-content">
      <div class="footer-section">
        <h4>XIII Mostra do Conhecimento</h4>
        <p>e VI Feira de Oportunidades</p>
        <p class="footer-date">29/09 a 04/10 de 2025</p>
      </div>
      <div class="footer-section">
        <h4>Sistema de Avaliação</h4>
        <p>Plataforma digital para avaliação de trabalhos científicos</p>
        <p class="footer-version">Versão 1.0</p>
      </div>
      <div class="footer-section">
        <h4>Suporte</h4>
        <p>Para dúvidas ou problemas técnicos, entre em contato com a equipe de TI</p>
        <p class="footer-contact">ti@example.com</p>
      </div>
    </div>
    <div class="footer-bottom">
      <p>&copy; 2025 - Todos os direitos reservados</p>
    </div>
  </footer>
</template>

<script setup>
// Props para controlar o comportamento do footer
defineProps({
  fullWidth: {
    type: Boolean,
    default: false
  }
})
</script>

<style scoped>
.standalone-footer {
  background: #17635A;
  color: #fff;
  padding: 2rem 1rem 1rem 1rem;
  margin-top: auto;
  width: 100%;
}

.standalone-footer.full-width {
  width: 100vw;
  margin-left: calc(-50vw + 50%);
  margin-right: calc(-50vw + 50%);
}

.footer-content {
  max-width: 1100px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-bottom: 1.5rem;
}

.footer-section h4 {
  color: #CFE3C6;
  font-size: 1.1rem;
  font-weight: 700;
  margin-bottom: 0.8rem;
}

.footer-section p {
  color: #fff;
  font-size: 0.9rem;
  line-height: 1.5;
  margin-bottom: 0.5rem;
}

.footer-date {
  color: #CFE3C6 !important;
  font-weight: 600;
  font-size: 0.95rem !important;
}

.footer-version {
  color: #CFE3C6 !important;
  font-size: 0.85rem !important;
  font-style: italic;
}

.footer-contact {
  color: #4CB050 !important;
  font-weight: 600;
}

.footer-bottom {
  border-top: 1px solid #4CB050;
  padding-top: 1rem;
  text-align: center;
}

.footer-bottom p {
  color: #CFE3C6;
  font-size: 0.85rem;
  margin: 0;
}

@media (max-width: 700px) {
  .standalone-footer {
    padding: 1.5rem 0.5rem 1rem 0.5rem;
  }
  .footer-content {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  .footer-section {
    text-align: center;
  }
}
</style>
