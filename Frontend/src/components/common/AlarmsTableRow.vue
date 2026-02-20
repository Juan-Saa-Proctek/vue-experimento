<template>
  <div class="table-row" :class="alarm.active ? alarm.severity : 'resolved'">
    <div class="severity-cell">
      <div class="severity-dot" :class="alarm.active ? alarm.severity : 'resolved'"></div>
      <span>{{ severityLabel[alarm.severity] }}</span>
    </div>
    <div class="asset-cell">
      <span class="asset-tag-small">{{ alarm.assetTag }}</span>
      <span class="asset-name-small">{{ alarm.assetName }}</span>
    </div>
    <div class="message-cell">{{ alarm.message }}</div>
    <div class="rms-cell" :class="alarm.active ? alarm.severity : 'resolved'">
      {{ Number(alarm.rmsValue).toFixed(2) }} mm/s
    </div>
    <div class="date-cell">{{ formatDate(alarm.timestamp) }}</div>
    <div class="status-cell">
      <span v-if="alarm.active" class="active-badge">Activa</span>
      <span v-else class="resolved-badge">Resuelta</span>
    </div>
  </div>
</template>

<script setup>
defineProps({
  alarm:      { type: Object,   required: true },
  formatDate: { type: Function, required: true }
})

const severityLabel = {
  critical: 'Crítico',
  warning:  'Advertencia'
}
</script>

<style scoped>
.table-row {
  display: grid;
  grid-template-columns: 110px 160px minmax(200px, 1fr) 120px 160px 100px;
  padding: 14px 20px;
  border-top: 1px solid var(--color-surface2);
  align-items: center;
  transition: background 0.2s;
}

.table-row:hover { background-color: rgba(255,255,255,0.03); }

/* Border izquierdo por estado */
.table-row.critical { border-left: 3px solid var(--color-critical); }
.table-row.warning  { border-left: 3px solid var(--color-warning); }
.table-row.resolved { border-left: 3px solid var(--color-normal); }

.severity-cell {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--color-text-dark);
}

/* Dot de severidad */
.severity-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}

.severity-dot.critical { background-color: var(--color-critical); }
.severity-dot.warning  { background-color: var(--color-warning); }
.severity-dot.resolved { background-color: var(--color-normal); }

.asset-cell {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.asset-tag-small {
  font-size: 13px;
  font-weight: 700;
  color: var(--color-text-dark);
  font-family: monospace;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 160px;
}

.asset-name-small {
  font-size: 11px;
  color: var(--color-text-muted);
}

.message-cell {
  font-size: 13px;
  color: var(--color-text-dark);
}

/* RMS color por estado */
.rms-cell {
  font-size: 13px;
  font-weight: 600;
}

.rms-cell.critical { color: var(--color-critical); }
.rms-cell.warning  { color: var(--color-warning); }
.rms-cell.resolved { color: var(--color-normal); }

.date-cell {
  font-size: 12px;
  color: var(--color-text-dark);
}

/* Badges */
.active-badge {
  background-color: rgba(255, 68, 68, 0.15);
  color: var(--color-critical);
  padding: 3px 10px;
  border-radius: 10px;
  font-size: 11px;
  font-weight: 600;
}

.resolved-badge {
  background-color: rgba(0, 200, 81, 0.15);
  color: var(--color-normal);
  padding: 3px 10px;
  border-radius: 10px;
  font-size: 11px;
  font-weight: 600;
}
</style>