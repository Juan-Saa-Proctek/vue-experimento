<template>
  <button class="base-btn" :class="[variant, size]" v-bind="$attrs">
    <slot />
  </button>
</template>

<script setup>
defineProps({
  variant: {
    type: String,
    default: 'default'
    // default | primary | danger
  },
  size: {
    type: String,
    default: 'md'
    // sm | md | lg
  }
})
</script>

<style scoped>
.base-btn {
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: opacity 0.2s, background 0.2s;
}

.base-btn:hover { opacity: 0.85; }

/* Variantes */
.base-btn.default {
  background-color: var(--color-surface2);
  color: var(--color-text);
}

.base-btn.primary {
  background-color: var(--color-accent);
  color: white;
}

.base-btn.danger {
  background-color: var(--color-critical);
  color: white;
}

/* Tamaños */
.base-btn.sm { padding: 6px 12px; font-size: 12px; }
.base-btn.md { padding: 8px 16px; font-size: 13px; }
.base-btn.lg { padding: 12px 24px; font-size: 15px; }
</style>