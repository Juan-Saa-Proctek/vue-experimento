<template>
  <div class="alarms-view">

    <LoadingSpinner v-if="alarmsStore.loading" message="Cargando alarmas..." />

    <ErrorState
      v-else-if="alarmsStore.error"
      :message="alarmsStore.error"
      retryable
      @retry="alarmsStore.fetchAlarms"
    />

    <template v-else>

      <!-- Resumen -->
      <div class="alarms-summary">
        <div class="summary-card critical">
          <span class="summary-count">{{ criticalCount }}</span>
          <span class="summary-label">Críticas</span>
        </div>
        <div class="summary-card warning">
          <span class="summary-count">{{ warningCount }}</span>
          <span class="summary-label">Advertencias</span>
        </div>
        <div class="summary-card resolved">
          <span class="summary-count">{{ resolvedCount }}</span>
          <span class="summary-label">Resueltas</span>
        </div>
      </div>

      <!-- Filtros -->
      <div class="filters">
        <button
          v-for="f in filters"
          :key="f.key"
          class="filter-btn"
          :class="{ active: activeFilter === f.key }"
          @click="activeFilter = f.key"
        >
          {{ f.label }}
        </button>
      </div>

      <!-- Tabla -->
      <div class="alarms-table">
        <div class="table-header">
          <span>Severidad</span>
          <span>Equipo</span>
          <span>Mensaje</span>
          <span>Valor RMS</span>
          <span>Fecha</span>
          <span>Estado</span>
        </div>

        <div v-if="filteredAlarms.length === 0" class="empty-state">
          No hay alarmas registradas.
        </div>

        <AlarmsTableRow
          v-for="alarm in filteredAlarms"
          :key="alarm.id"
          :alarm="alarm"
          :formatDate="formatDate"
        />
      </div>

    </template>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAlarmsStore } from '../stores/alarmsStore.js'
import LoadingSpinner  from '../components/common/LoadingSpinner.vue'
import ErrorState      from '../components/common/ErrorState.vue'
import AlarmsTableRow  from '../components/common/AlarmsTableRow.vue'

const alarmsStore = useAlarmsStore()
const activeFilter = ref('all')

const filters = [
  { key: 'all',      label: 'Todas' },
  { key: 'active',   label: 'Activas' },
  { key: 'critical', label: 'Críticas' },
  { key: 'warning',  label: 'Advertencias' },
  { key: 'resolved', label: 'Resueltas' },
]

const filteredAlarms = computed(() => {
  const all = alarmsStore.alarms
  if (activeFilter.value === 'all')      return all
  if (activeFilter.value === 'active')   return all.filter(a => a.active)
  if (activeFilter.value === 'resolved') return all.filter(a => !a.active)
  return all.filter(a => a.severity === activeFilter.value)
})

const criticalCount = computed(() =>
  alarmsStore.alarms.filter(a => a.severity === 'critical' && a.active).length
)
const warningCount = computed(() =>
  alarmsStore.alarms.filter(a => a.severity === 'warning' && a.active).length
)
const resolvedCount = computed(() =>
  alarmsStore.alarms.filter(a => !a.active).length
)

function formatDate(iso) {
  return new Date(iso).toLocaleString('es-CO', {
    day: '2-digit', month: '2-digit', year: 'numeric',
    hour: '2-digit', minute: '2-digit'
  })
}

onMounted(() => alarmsStore.fetchAlarms())
</script>

<style scoped>
.alarms-view {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.alarms-summary {
  display: flex;
  gap: 16px;
}

.summary-card {
  background-color: var(--color-surface3);
  border-radius: 12px;
  padding: 20px 32px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  border: 1px solid var(--color-surface);
  min-width: 140px;
}

.summary-card.critical { border-top: 3px solid var(--color-critical); }
.summary-card.warning  { border-top: 3px solid var(--color-warning); }
.summary-card.resolved { border-top: 3px solid var(--color-normal); }

.summary-count {
  font-size: 36px;
  font-weight: 700;
}

.summary-card.critical .summary-count { color: var(--color-critical); }
.summary-card.warning  .summary-count { color: var(--color-warning); }
.summary-card.resolved .summary-count { color: var(--color-normal); }

.summary-label {
  font-size: 12px;
  color: var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.filters {
  display: flex;
  gap: 8px;
}

.filter-btn {
  background: var(--color-surface3);
  border: 1px solid var(--color-surface);
  color: var(--color-text-muted);
  padding: 8px 18px;
  border-radius: 20px;
  cursor: pointer;
  font-size: 13px;
  transition: all 0.2s;
}

.filter-btn:hover,
.filter-btn.active {
  background: var(--color-surface4);
  color: var(--color-text-dark);
  border-color: var(--color-accent);
}

.alarms-table {
  background-color: var(--color-surface3);
  border-radius: 12px;
  border: 1px solid var(--color-surface);
  overflow: hidden;
}

.table-header {
  display: grid;
  grid-template-columns: 130px 180px 1fr 120px 160px 100px;
  padding: 12px 20px;
  background-color: var(--color-surface3);
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: var(--color-text-muted);
}

.empty-state {
  text-align: center;
  padding: 60px;
  color: var(--color-text-muted);
  font-size: 15px;
}
</style>