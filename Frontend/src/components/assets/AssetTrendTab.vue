<template>
  <div class="chart-card">
    <div class="chart-card-header">
      <h3>Tendencia RMS Histórica</h3>
    </div>
    <TrendChart :data="trendData" :limit="rmsLimit" />
  </div>
</template>

<script setup>
import TrendChart from '../charts/TrendChart.vue'

defineProps({
  trendData: { type: Array,  required: true },
  rmsLimit:  { type: Number, required: true }
})
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
</style>