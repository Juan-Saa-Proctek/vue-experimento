<template>
  <div class="error-wrapper">
    <span class="error-icon">⚠️</span>
    <p class="error-message">{{ message }}</p>
    <BaseButton v-if="retryable" variant="primary" @click="$emit('retry')">
      Reintentar
    </BaseButton>
  </div>
</template>

<script setup>
import BaseButton from './BaseButton.vue'

defineProps({
  message:   { type: String, default: 'Ocurrió un error inesperado.' },
  retryable: { type: Boolean, default: false }
})

defineEmits(['retry'])
</script>

<style scoped>
.error-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 60px;
}

.error-icon {
  font-size: 40px;
}

.error-message {
  font-size: 15px;
  color: var(--color-text-muted);
  text-align: center;
}
</style>