<template>
  <Teleport to="body">
    <div class="modal-overlay" @click.self="$emit('close')">
      <div class="modal">
        <div class="modal-header">
          <div>
            <h3>Espectro FFT</h3>
            <span class="modal-subtitle">{{ time }} · RMS: {{ value }} mm/s</span>
          </div>
          <button class="close-btn" @click="$emit('close')">✕</button>
        </div>
        <div class="modal-body">
          <FFTChart
            :data="fftData"
            :frequencies="frequencies"
            :rpmNominal="rpmNominal"
          />
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import FFTChart from '../charts/FFTChart.vue'

defineProps({
  time:       { type: String, default: '' },
  value:      { type: Number, default: 0 },
  fftData:    { type: Array,  default: () => [] },
  frequencies:{ type: Array,  default: () => [] },
  rpmNominal: { type: Number, default: 1750 }
})

defineEmits(['close'])
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(2px);
}

.modal {
  background-color: var(--color-surface4);
  border-radius: 16px;
  padding: 24px;
  border: 1px solid var(--color-surface);
  width: 680px;
  max-width: 95vw;
  box-shadow: 0 20px 60px rgba(0,0,0,0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
}

.modal-header h3 {
  font-size: 16px;
  font-weight: 700;
  color: var(--color-text-dark);
}

.modal-subtitle {
  font-size: 12px;
  color: var(--color-text-muted);
  margin-top: 4px;
  display: block;
}

.close-btn {
  background: var(--color-surface);
  border: none;
  color: var(--color-text);
  width: 32px;
  height: 32px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s;
}

.close-btn:hover { background: var(--color-surface2); }

.modal-body {
  width: 100%;
}
</style>