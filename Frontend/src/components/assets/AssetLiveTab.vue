<template>
  <div class="charts-grid">
    <div class="chart-card">
      <div class="chart-card-header">
        <h3>Forma de Onda en Tiempo Real</h3>
        <span class="live-indicator">● EN VIVO</span>
      </div>
      <WaveformChart :data="waveformData" />
    </div>
    <div class="chart-card">
      <div class="chart-card-header">
        <h3>Espectro de Frecuencias (FFT)</h3>
      </div>
      <FFTChart :data="fftData" :frequencies="fftFrequencies" />
    </div>
  </div>
</template>

<script setup>
import WaveformChart from '../charts/WaveformChart.vue'
import FFTChart from '../charts/FFTChart.vue'

defineProps({
  waveformData:   { type: Array, required: true },
  fftData:        { type: Array, required: true },
  fftFrequencies: { type: Array, required: true }
})
</script>

<style scoped>
.charts-grid {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

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

.live-indicator {
  font-size: 12px;
  color: var(--color-normal);
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.3; }
}
</style>