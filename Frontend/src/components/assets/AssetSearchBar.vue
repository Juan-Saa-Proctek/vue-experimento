<template>
  <div class="search-controls">
    <div class="search-box">
      <Search :size="16" color="var(--color-text-dark)" />
      <input 
        :value="modelValue"
        @input="$emit('update:modelValue', $event.target.value)"
        type="text" 
        placeholder="Buscar por tag, nombre o ubicación..."
        class="search-input"
      />
    </div>
    <select 
      :value="filterStatus"
      @change="$emit('update:filterStatus', $event.target.value)"
      class="filter-select"
    >
      <option value="">Todos los estados</option>
      <option value="normal">Normal</option>
      <option value="warning">Advertencia</option>
      <option value="critical">Crítico</option>
      <option value="offline">Desconectado</option>
    </select>
  </div>
</template>

<script setup>
import { Search } from 'lucide-vue-next'

defineProps({
  modelValue: { type: String, default: '' },
  filterStatus: { type: String, default: '' }
})

defineEmits(['update:modelValue', 'update:filterStatus'])
</script>

<style scoped>
.search-controls {
  display: flex;
  gap: 12px;
  align-items: center;
}

.search-box {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background-color: var(--color-surface4);
  border: 1px solid var(--color-surface);
  border-radius: 8px;
}

.search-input {
  flex: 1;
  background: transparent;
  border: none;
  color: var(--color-text-dark);
  font-size: 13px;
  outline: none;
}

.filter-select {
  padding: 8px 12px;
  background-color: var(--color-surface4);
  border: 1px solid var(--color-surface);
  border-radius: 8px;
  color: var(--color-text-dark);
  font-size: 13px;
  outline: none;
}
</style>