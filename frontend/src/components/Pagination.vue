<template>
  <div class="pagination-container">
    <div class="pagination-info">
      <span>Mostrando {{ startItem }}-{{ endItem }} de {{ total }} itens</span>
    </div>

    <div class="pagination-controls">
      <button
        @click="goToPage(currentPage - 1)"
        :disabled="!hasPrev"
        class="pagination-btn"
      >
        Anterior
      </button>

            <div class="page-numbers">
        <template v-for="pageNum in visiblePages" :key="pageNum">
          <button
            v-if="pageNum !== '...'"
            @click="goToPage(pageNum)"
            :class="['page-btn', { active: pageNum === currentPage }]"
          >
            {{ pageNum }}
          </button>
          <span v-else class="page-ellipsis">...</span>
        </template>
      </div>

      <button
        @click="goToPage(currentPage + 1)"
        :disabled="!hasNext"
        class="pagination-btn"
      >
        Próximo
      </button>
    </div>

    <div class="per-page-selector">
      <label>Itens por página:</label>
      <select v-model="currentPerPage" @change="onPerPageChange">
        <option value="10">10</option>
        <option value="20">20</option>
        <option value="30">30</option>
        <option value="40">40</option>
        <option value="50">50</option>
      </select>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'

const props = defineProps({
  pagination: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['page-change', 'per-page-change'])

const currentPage = ref(props.pagination.page || 1)
const currentPerPage = ref(props.pagination.per_page || 20)

const total = computed(() => props.pagination.total || 0)
const pages = computed(() => props.pagination.pages || 1)
const hasPrev = computed(() => props.pagination.has_prev || false)
const hasNext = computed(() => props.pagination.has_next || false)

const startItem = computed(() => {
  if (total.value === 0) return 0
  return (currentPage.value - 1) * currentPerPage.value + 1
})

const endItem = computed(() => {
  return Math.min(currentPage.value * currentPerPage.value, total.value)
})

const visiblePages = computed(() => {
  const pageNumbers = []
  const maxVisible = 5

  if (pages.value <= maxVisible) {
    for (let i = 1; i <= pages.value; i++) {
      pageNumbers.push(i)
    }
  } else {
    // Maximum 5 elements: current page + context
    if (currentPage.value === 1) {
      pageNumbers.push(1, 2, 3, '...', pages.value)
    } else if (currentPage.value === pages.value) {
      pageNumbers.push(1, '...', pages.value - 2, pages.value - 1, pages.value)
    } else if (currentPage.value === 2) {
      pageNumbers.push(1, 2, 3, '...', pages.value)
    } else if (currentPage.value === pages.value - 1) {
      pageNumbers.push(1, '...', pages.value - 2, pages.value - 1, pages.value)
    } else {
      pageNumbers.push(1, '...', currentPage.value - 1, currentPage.value, currentPage.value + 1, '...', pages.value)

      if (pageNumbers.length > maxVisible) {
        pageNumbers.splice(-2, 2)
      }
    }
  }

  return pageNumbers
})

function goToPage(page) {
  if (page >= 1 && page <= pages.value && page !== currentPage.value) {
    currentPage.value = page
    emit('page-change', page)
  }
}

function onPerPageChange() {
  currentPage.value = 1
  emit('per-page-change', currentPerPage.value)
}

watch(() => props.pagination.page, (newPage) => {
  currentPage.value = newPage
})

watch(() => props.pagination.per_page, (newPerPage) => {
  currentPerPage.value = newPerPage
})
</script>

<style scoped>
.pagination-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 1.5rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

.pagination-info {
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 0.9rem;
  color: #6c757d;
}

.per-page-selector {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  justify-content: center;
  margin-top: 1rem;
}

.per-page-selector label {
  font-size: 0.85rem;
  color: #495057;
}

.per-page-selector select {
  padding: 0.3rem 0.5rem;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 0.85rem;
  background: white;
}

.pagination-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.5rem;
}

.pagination-btn {
  padding: 0.5rem 1rem;
  border: 1px solid #dee2e6;
  background: white;
  color: #495057;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.pagination-btn:hover:not(:disabled) {
  background: #e9ecef;
  border-color: #adb5bd;
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-numbers {
  display: flex;
  gap: 0.25rem;
}

.page-btn {
  padding: 0.5rem 0.75rem;
  border: 1px solid #dee2e6;
  background: white;
  color: #495057;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  min-width: 2.5rem;
  transition: all 0.2s;
}

.page-btn:hover {
  background: #e9ecef;
  border-color: #adb5bd;
}

.page-btn.active {
  background: #17635A;
  color: white;
  border-color: #17635A;
}

.page-btn.active:hover {
  background: #4CB050;
  border-color: #4CB050;
}

.page-ellipsis {
  padding: 0.5rem 0.75rem;
  color: #6c757d;
  font-size: 0.9rem;
  min-width: 2.5rem;
  text-align: center;
  user-select: none;
}

@media (max-width: 768px) {
  .pagination-container {
    padding: 0.8rem;
    gap: 0.8rem;
  }

  .pagination-info {
    flex-direction: column;
    gap: 0.5rem;
    align-items: flex-start;
  }

  .pagination-controls {
    flex-wrap: wrap;
    gap: 0.3rem;
  }

  .page-btn {
    padding: 0.4rem 0.6rem;
    font-size: 0.85rem;
    min-width: 2rem;
  }

  .pagination-btn {
    padding: 0.4rem 0.8rem;
    font-size: 0.85rem;
  }
}

@media (max-width: 480px) {
  .pagination-container {
    padding: 0.6rem;
    gap: 0.6rem;
  }

  .page-numbers {
    gap: 0.2rem;
  }

  .page-btn {
    padding: 0.3rem 0.5rem;
    font-size: 0.8rem;
    min-width: 1.8rem;
  }

  .pagination-btn {
    padding: 0.3rem 0.6rem;
    font-size: 0.8rem;
  }
}
</style>
