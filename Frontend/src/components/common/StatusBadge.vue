<template>
  <span class="badge" :class="status">{{ label }}</span>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  status: {
    type: String,
    required: true
  }
})

const labels = {
  normal:   'Normal',
  warning:  'Advertencia',
  critical: 'Crítico',
  offline:  'Desconectado'
}

const label = computed(() => labels[props.status] || props.status)
</script>

<style scoped>
.badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.badge.normal {
  background-color: rgba(1, 167, 67, 0.15);
  color: var(--color-normal);
}

.badge.warning {
  background-color: rgba(255, 187, 51, 0.2);
  color: var(--color-warning);
}

.badge.critical {
  background-color: rgba(255, 68, 68, 0.15);
  color: var(--color-critical);
  animation: pulse 2s infinite;
}

.badge.offline {
  background-color: rgba(23, 45, 226, 0.15);
  color: var(--color-offline);
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}
</style>