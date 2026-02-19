<template>
  <div class="chart-card">
    <div class="chart-card-header">
      <h3>Tendencia RMS</h3>
      <span v-if="selectedPoint" class="selected-info">
        <GitCommitHorizontal :size="20" /> {{ selectedPoint.time }} → {{ selectedPoint.value }} mm/s
      </span>
    </div>
    <TrendChart
      :data="trendData"
      :limit="rmsLimit"
      @point-click="onPointClick"
    />
    <p class="trend-hint">
      <GitCommitHorizontal :size="20" />
      Haz clic en un punto para ver el FFT de ese momento
   </p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import TrendChart from '../charts/TrendChart.vue'

import { GitCommitHorizontal } from 'lucide-vue-next';

defineProps({
  trendData: { type: Array,  required: true },
  rmsLimit:  { type: Number, required: true }
})

const emit = defineEmits(['point-click'])
const selectedPoint = ref(null)

function onPointClick(point) {
  selectedPoint.value = point
  emit('point-click', point)   
}
</script>

<style scoped>
.chart-card {
  background-color: var(--color-surface4);
  border-radius: 12px;
  padding: 20px;
  border: 1px solid var(--color-surface);
}

.chart-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.chart-card-header h3 {
  color: var(--color-text-dark);
  font-size: 15px;
}

.selected-info {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: var(--color-accent);
  font-weight: 600;
}

.trend-hint {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: var(--color-text-muted);
  margin-top: 8px;
  text-align: center;
}
</style>