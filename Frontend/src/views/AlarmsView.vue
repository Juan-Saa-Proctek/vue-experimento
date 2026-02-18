<template>
  <div class="alarms-view">

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

    <!-- Lista de alarmas -->
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

      <div
        v-for="alarm in filteredAlarms"
        :key="alarm.id"
        class="table-row"
        :class="alarm.severity"
      >
        <div class="severity-cell">
          <div class="severity-dot" :class="alarm.severity"></div>
          <span>{{ severityLabel[alarm.severity] }}</span>
        </div>
        <div class="asset-cell">
          <span class="asset-tag-small">{{ alarm.assetTag }}</span>
          <span class="asset-name-small">{{ alarm.assetName }}</span>
        </div>
        <div class="message-cell">{{ alarm.message }}</div>
        <div class="rms-cell" :class="alarm.severity">{{ alarm.rmsValue }} mm/s</div>
        <div class="date-cell">{{ formatDate(alarm.timestamp) }}</div>
        <div class="status-cell">
          <span v-if="alarm.active" class="active-badge">Activa</span>
          <span v-else class="resolved-badge">Resuelta</span>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAlarmsStore } from '../stores/alarmsStore.js'

const alarmsStore = useAlarmsStore()

const activeFilter = ref('all')

const filters = [
  { key: 'all',      label: 'Todas' },
  { key: 'active',   label: 'Activas' },
  { key: 'critical', label: 'Críticas' },
  { key: 'warning',  label: 'Advertencias' },
  { key: 'resolved', label: 'Resueltas' },
]

const severityLabel = {
  critical: 'Crítico',
  warning:  'Advertencia'
}

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
  background-color: var(--color-surface);
  border-radius: 12px;
  padding: 20px 32px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  border: 1px solid var(--color-surface2);
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
  background: var(--color-surface);
  border: 1px solid var(--color-surface2);
  color: var(--color-text-muted);
  padding: 8px 18px;
  border-radius: 20px;
  cursor: pointer;
  font-size: 13px;
  transition: all 0.2s;
}

.filter-btn:hover,
.filter-btn.active {
  background: var(--color-surface2);
  color: var(--color-text);
  border-color: var(--color-accent);
}

.alarms-table {
  background-color: var(--color-surface);
  border-radius: 12px;
  border: 1px solid var(--color-surface2);
  overflow: hidden;
}

.table-header {
  display: grid;
  grid-template-columns: 130px 180px 1fr 120px 160px 100px;
  padding: 12px 20px;
  background-color: var(--color-surface2);
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: var(--color-text-muted);
}

.table-row {
  display: grid;
  grid-template-columns: 130px 180px 1fr 120px 160px 100px;
  padding: 14px 20px;
  border-top: 1px solid var(--color-surface2);
  align-items: center;
  transition: background 0.2s;
}

.table-row:hover {
  background-color: rgba(255,255,255,0.03);
}

.table-row.critical {
  border-left: 3px solid var(--color-critical);
}

.table-row.warning {
  border-left: 3px solid var(--color-warning);
}

.severity-cell {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--color-text);
}

.severity-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}

.severity-dot.critical { background-color: var(--color-critical); }
.severity-dot.warning  { background-color: var(--color-warning); }

.asset-cell {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.asset-tag-small {
  font-size: 13px;
  font-weight: 700;
  color: var(--color-text);
  font-family: monospace;
}

.asset-name-small {
  font-size: 11px;
  color: var(--color-text-muted);
}

.message-cell {
  font-size: 13px;
  color: var(--color-text);
}

.rms-cell {
  font-size: 13px;
  font-weight: 600;
}

.rms-cell.critical { color: var(--color-critical); }
.rms-cell.warning  { color: var(--color-warning); }

.date-cell {
  font-size: 12px;
  color: var(--color-text-muted);
}

.active-badge {
  background-color: rgba(255,68,68,0.15);
  color: var(--color-critical);
  padding: 3px 10px;
  border-radius: 10px;
  font-size: 11px;
  font-weight: 600;
}

.resolved-badge {
  background-color: rgba(0,200,81,0.15);
  color: var(--color-normal);
  padding: 3px 10px;
  border-radius: 10px;
  font-size: 11px;
  font-weight: 600;
}

.empty-state {
  text-align: center;
  padding: 60px;
  color: var(--color-text-muted);
  font-size: 15px;
}
</style>