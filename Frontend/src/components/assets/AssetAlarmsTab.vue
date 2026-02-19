<template>
  <div class="alarms-list">
    <div v-if="alarms.length === 0" class="empty-state">
      No hay alarmas registradas para este equipo.
    </div>
    <AlarmRow
      v-for="alarm in alarms"
      :key="alarm.id"
      :alarm="alarm"
      :formatDate="formatDate"
    />
  </div>
</template>

<script setup>
import AlarmRow from '../common/AlarmRow.vue'

defineProps({
  alarms:     { type: Array,    required: true },
  formatDate: { type: Function, required: true }
})
</script>

<style scoped>
.alarms-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.empty-state {
  text-align: center;
  color: var(--color-text-muted);
  padding: 60px;
  font-size: 16px;
}
</style>