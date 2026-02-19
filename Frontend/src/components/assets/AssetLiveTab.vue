<template>
  <div class="live-layout">

    <!-- Gauge RMS -->
    <div class="chart-card gauge-card">
      <div class="chart-card-header">
        <h3>RMS Actual</h3>
        <span class="live-indicator">● EN VIVO</span>
      </div>
      <GaugeChart
        :value="asset.rmsActual"
        :limit="asset.rmsLimit"
        :status="asset.status"
      />
    </div>

    <!-- Waveform -->
    <div class="chart-card waveform-card">
      <div class="chart-card-header">
        <h3>Forma de Onda</h3>
      </div>
      <WaveformChart :data="waveformData" :status="asset.status" />
    </div>

    <!-- FFT -->
    <div class="chart-card fft-card">
      <div class="chart-card-header">
        <h3>Espectro FFT</h3>
      </div>
      <FFTChart
        :data="fftData"
        :frequencies="fftFrequencies"
        :rpmNominal="asset.rpmNominal"
      />
    </div>

  </div>
</template>

<script setup>
import WaveformChart from '../charts/WaveformChart.vue'
import FFTChart      from '../charts/FFTChart.vue'
import GaugeChart    from '../charts/GaugeChart.vue'

defineProps({
  asset:          { type: Object, required: true },
  waveformData:   { type: Array,  required: true },
  fftData:        { type: Array,  required: true },
  fftFrequencies: { type: Array,  required: true }
})
</script>

<style scoped>
.live-layout {
  display: grid;
  grid-template-columns: 250px 1fr;
  grid-template-rows: auto auto;
  gap: 16px;
}

.gauge-card {
  grid-column: 1;
  grid-row: 1 / 3;
}

.waveform-card {
  grid-column: 2;
  grid-row: 1;
}

.fft-card {
  grid-column: 2;
  grid-row: 2;
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
  margin-bottom: 12px;
}

.chart-card-header h3 {
  color: var(--color-text-dark);
  font-size: 14px;
  font-weight: 600;
}

.hint {
  font-size: 11px;
  color: var(--color-text-muted);
  font-weight: 400;
}

.live-indicator {
  font-size: 12px;
  color: var(--color-normal);
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50%       { opacity: 0.3; }
}
</style>