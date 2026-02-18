<template>
  <div class="asset-card" :class="asset.status" @click="goToDetail">
    <div class="card-header">
      <div class="asset-tag">{{ asset.tag }}</div>
      <StatusBadge :status="asset.status" />
    </div>

    <div class="asset-name">{{ asset.name }}</div>
    <div class="asset-type">{{ asset.type }}</div>

    <div class="asset-metrics">
      <div class="metric">
        <span class="metric-label">RMS Actual</span>
        <span class="metric-value" :class="asset.status">{{ asset.rmsActual.toFixed(2) }} mm/s</span>
      </div>
      <div class="metric">
        <span class="metric-label">Límite</span>
        <span class="metric-value">{{ asset.rmsLimit }} mm/s</span>
      </div>
      <div class="metric">
        <span class="metric-label">RPM Nominal</span>
        <span class="metric-value">{{ asset.rpmNominal }}</span>
      </div>
    </div>

    <div class="rms-bar-container">
      <div
        class="rms-bar"
        :class="asset.status"
        :style="{ width: barWidth + '%' }"
      ></div>
    </div>

    <div class="card-footer">
      <span class="location">📍 {{ asset.location }}</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import StatusBadge from '../common/StatusBadge.vue'

const props = defineProps({
  asset: {
    type: Object,
    required: true
  }
})

const router = useRouter()

function goToDetail() {
  router.push({ name: 'AssetDetail', params: { id: props.asset.id } })
}

const barWidth = computed(() => {
  const pct = (props.asset.rmsActual / props.asset.rmsLimit) * 100
  return Math.min(pct, 100)
})
</script>

<style scoped>
.asset-card {
  background-color: var(--color-surface4); /* Este es el color del Fondo de las Tarjetas de Activo */
  border-radius: 12px;
  padding: 20px;
  cursor: pointer;
  border: 1px solid var(--color-surface2);
  border-left: 4px solid var(--color-offline);
  transition: transform 0.2s, box-shadow 0.2s;
}

.asset-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.3);
}

.asset-card.normal   { border-left-color: var(--color-normal); }
.asset-card.warning  { border-left-color: var(--color-warning); }
.asset-card.critical { border-left-color: var(--color-critical); }
.asset-card.offline  { border-left-color: var(--color-offline); }

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.asset-tag {
  font-size: 20px;
  font-weight: 700;
  color: var(--color-text-dark);
  font-family: monospace;
}

.asset-name {
  font-size: 15px;
  font-weight: 600;
  color: var(--color-text-dark);
  margin-bottom: 4px;
}

.asset-type {
  font-size: 12px;
  color: var(--color-text-subtle);
  margin-bottom: 16px;
}

.asset-metrics {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
}

.metric {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.metric-label {
  font-size: 11px;
  color: var(--color-text-dark);
  text-transform: uppercase;
}

.metric-value {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text-dark);
}

.metric-value.normal   { color: var(--color-normal); }
.metric-value.warning  { color: var(--color-warning); }
.metric-value.critical { color: var(--color-critical); }

.rms-bar-container {
  height: 4px;
  background-color: var(--color-surface2);
  border-radius: 2px;
  margin-bottom: 16px;
  overflow: hidden;
}

.rms-bar {
  height: 100%;
  border-radius: 2px;
  transition: width 0.5s ease;
}

.rms-bar.normal   { background-color: var(--color-normal); }
.rms-bar.warning  { background-color: var(--color-warning); }
.rms-bar.critical { background-color: var(--color-critical); }
.rms-bar.offline  { background-color: var(--color-offline); }

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.location {
  font-size: 12px;
  color: var(--color-text-dark);
}
</style>