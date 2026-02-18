<template>
  <div class="base-card" :class="{ clickable }">
    <slot />
  </div>
</template>

<script setup>
defineProps({
  clickable: { type: Boolean, default: false }
})
</script>

<style scoped>
.base-card {
  background-color: var(--color-surface);
  border-radius: 12px;
  padding: 20px;
  border: 1px solid var(--color-surface2);
}

.base-card.clickable {
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.base-card.clickable:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.3);
}
</style>