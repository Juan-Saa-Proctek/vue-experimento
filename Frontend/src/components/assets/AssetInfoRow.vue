<template>
  <div class="info-row">
    <span class="info-label">{{ label }}</span>
    <span class="info-value" :class="highlight">{{ value }}</span>
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
.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 14px;
  border-radius: 8px;
  background-color: var(--color-surface4);
  border: 1px solid var(--color-surface);
  transition: background 0.2s;
}

.info-row:hover {
  background-color: var(--color-surface3);
}

.info-label {
  font-size: 13px;
  font-weight: 600;
  color: var(--color-text-dark);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.info-value {
  font-size: 13px;
  font-weight: 600;
  color: var(--color-text-dark);
  background-color: var(--color-surface4);
  padding: 2px 10px;
  border-radius: 6px;
}

.info-value.normal   { color: var(--color-normal);   background-color: rgba(0, 200, 100, 0.1); }
.info-value.warning  { color: var(--color-warning);  background-color: rgba(255, 180, 0, 0.1); }
.info-value.critical { color: var(--color-critical); background-color: rgba(255, 68, 68, 0.1); }
.info-value.offline  { color: var(--color-offline);  background-color: rgba(150, 150, 150, 0.1); }
</style>