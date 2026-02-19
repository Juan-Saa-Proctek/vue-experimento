<template>
  <div class="alarm-row" :class="alarm.severity">
    <div class="alarm-severity-bar"></div>
    <div class="alarm-info">
      <div class="alarm-message">{{ alarm.message }}</div>
      <div class="alarm-meta">
        {{ formatDate(alarm.timestamp) }} · RMS: {{ alarm.rmsValue }} mm/s
      </div>
    </div>
    <StatusBadge :status="alarm.severity" />
  </div>
</template>

<script setup>
import StatusBadge from './StatusBadge.vue'

defineProps({
  alarm:      { type: Object,   required: true },
  formatDate: { type: Function, required: true }
})
</script>

<style scoped>
.alarm-row {
  display: flex;
  align-items: center;
  gap: 16px;
  background-color: var(--color-surface4);
  border-radius: 10px;
  padding: 14px 16px;
  border: 1px solid var(--color-surface);
}

.alarm-severity-bar {
  width: 4px;
  height: 40px;
  border-radius: 2px;
  flex-shrink: 0;
}

.alarm-row.warning  .alarm-severity-bar { background-color: var(--color-warning); }
.alarm-row.critical .alarm-severity-bar { background-color: var(--color-critical); }

.alarm-info { flex: 1; }

.alarm-message {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text-dark);
  margin-bottom: 4px;
}

.alarm-meta {
  font-size: 12px;
  color: var(--color-text-muted);
}
</style>