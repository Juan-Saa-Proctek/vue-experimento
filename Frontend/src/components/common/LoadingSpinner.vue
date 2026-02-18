<template>
  <div class="spinner-wrapper">
    <div class="spinner"></div>
    <span v-if="message" class="spinner-message">{{ message }}</span>
  </div>
</template>

<script setup>
defineProps({
  message: { type: String, default: '' }
})
</script>

<style scoped>
.spinner-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  padding: 60px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--color-surface2);
  border-top-color: var(--color-accent);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.spinner-message {
  font-size: 14px;
  color: var(--color-text-muted);
}
</style>