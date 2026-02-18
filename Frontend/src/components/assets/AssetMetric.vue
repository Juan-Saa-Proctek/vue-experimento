<template>
  <div class="metric">
    <span class="metric-label">{{ label }}</span>
    <span class="metric-value" :class="highlight">{{ value }}</span>
  </div>
</template>

<script setup>
defineProps({
  label:     { type: String, required: true },
  value:     { type: String, required: true },
  highlight: { type: String, default: '' }
})
</script>

<style scoped>
.metric {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.metric-label {
  font-size: 11px;
  color: var(--color-text-dark);
  text-transform: uppercase;
}

.metric-value {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text-dark);
}

.metric-value.normal   { color: var(--color-normal); }
.metric-value.warning  { color: var(--color-warning); }
.metric-value.critical { color: var(--color-critical); }
</style>