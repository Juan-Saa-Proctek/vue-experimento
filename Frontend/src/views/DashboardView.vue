<template>
  <div class="dashboard">

    <!-- Estado de carga -->
    <LoadingSpinner v-if="assetsStore.loading" message="Cargando equipos..." />

    <!-- Estado de error -->
    <ErrorState
      v-else-if="assetsStore.error"
      :message="assetsStore.error"
      retryable
      @retry="loadData"
    />

    <!-- Contenido normal -->
    <template v-else>

      <!-- Resumen superior -->
      <div class="summary-bar">
        <div
          v-for="item in summaryItems"
          :key="item.key"
          class="summary-item"
          :class="{ active: filterStatus === item.key }"
          @click="assetsStore.setFilter(item.key)"
        >
          <span class="summary-count" :style="{ color: item.color }">{{ item.count }}</span>
          <span class="summary-label">{{ item.label }}</span>
        </div>
      </div>

      <!-- Grid de equipos -->
      <div v-if="filteredAssets.length > 0" class="assets-grid">
        <AssetCard
          v-for="asset in filteredAssets"
          :key="asset.id"
          :asset="asset"
        />
      </div>

      <div v-else class="empty-state">
        No hay equipos con ese estado.
      </div>

    </template>

  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useAssetsStore } from '../stores/assetsStore.js'
import { useAlarmsStore } from '../stores/alarmsStore.js'
import AssetCard from '../components/assets/AssetCard.vue'
import LoadingSpinner from '../components/common/LoadingSpinner.vue'
import ErrorState from '../components/common/ErrorState.vue'

const assetsStore = useAssetsStore()
const alarmsStore = useAlarmsStore()

const filteredAssets = computed(() => assetsStore.filteredAssets)
const filterStatus   = computed(() => assetsStore.filterStatus)

const summaryItems = computed(() => [
  { key: 'all',      label: 'Todos',        count: assetsStore.summary.total,    color: 'var(--color-text)' },
  { key: 'normal',   label: 'Normal',       count: assetsStore.summary.normal,   color: 'var(--color-normal)' },
  { key: 'warning',  label: 'Advertencia',  count: assetsStore.summary.warning,  color: 'var(--color-warning)' },
  { key: 'critical', label: 'Crítico',      count: assetsStore.summary.critical, color: 'var(--color-critical)' },
  { key: 'offline',  label: 'Desconectado', count: assetsStore.summary.offline,  color: 'var(--color-offline)' },
])

// 🔧 FIX: Cargar assets Y alarmas juntos
async function loadData() {
  await Promise.all([
    assetsStore.fetchAssets(),
    alarmsStore.fetchAlarms(true) // true = solo activas
  ])
}

onMounted(() => loadData())
</script>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.summary-bar {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.summary-item {
  background-color: var(--color-surface3);
  border: 1px solid var(--color-surface);
  border-radius: 10px;
  padding: 14px 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  cursor: pointer;
  transition: all 0.2s;
  min-width: 110px;
}

.summary-item:hover,
.summary-item.active {
  border-color: var(--color-accent);
  background-color: var(--color-surface4);
}

.summary-count {
  font-size: 28px;
  font-weight: 700;
  line-height: 1;
}

.summary-label {
  font-size: 12px;
  color: var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.assets-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}

.empty-state {
  text-align: center;
  color: var(--color-text-muted);
  padding: 60px;
  font-size: 16px;
}
</style>