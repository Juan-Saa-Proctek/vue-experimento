<template>
  <div class="asset-detail" v-if="asset">

    <!-- Header del activo -->
    <div class="asset-header">
      <div class="asset-header-left">
        <button class="back-btn" @click="router.back()">← Volver</button>
        <div>
          <div class="asset-tag-title">{{ asset.tag }}</div>
          <div class="asset-name-title">{{ asset.name }}</div>
        </div>
      </div>
      <div class="asset-header-right">
        <div class="rms-display" :class="asset.status">
          <span class="rms-value">{{ asset.rmsActual.toFixed(2) }}</span>
          <span class="rms-unit">mm/s RMS</span>
        </div>
        <StatusBadge :status="asset.status" />
      </div>
    </div>

    <!-- Tabs -->
    <div class="tabs">
      <button
        v-for="tab in tabs"
        :key="tab.key"
        class="tab-btn"
        :class="{ active: activeTab === tab.key }"
        @click="activeTab = tab.key"
      >
        {{ tab.label }}
      </button>
    </div>

    <!-- Tab: Info -->
    <div v-if="activeTab === 'info'" class="tab-content">
      <div class="info-grid">
        <div class="info-card">
          <h3>Datos de Placa</h3>
          <div class="info-rows">
            <div class="info-row">
              <span class="info-label">Tag</span>
              <span class="info-value">{{ asset.tag }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Nombre</span>
              <span class="info-value">{{ asset.name }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Tipo</span>
              <span class="info-value">{{ asset.type }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Ubicación</span>
              <span class="info-value">{{ asset.location }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">RPM Nominal</span>
              <span class="info-value">{{ asset.rpmNominal }} RPM</span>
            </div>
            <div class="info-row">
              <span class="info-label">Límite RMS</span>
              <span class="info-value">{{ asset.rmsLimit }} mm/s</span>
            </div>
          </div>
        </div>

        <div class="info-card">
          <h3>Estado Actual</h3>
          <div class="info-rows">
            <div class="info-row">
              <span class="info-label">RMS Actual</span>
              <span class="info-value" :class="asset.status">{{ asset.rmsActual.toFixed(2) }} mm/s</span>
            </div>
            <div class="info-row">
              <span class="info-label">% del Límite</span>
              <span class="info-value" :class="asset.status">
                {{ ((asset.rmsActual / asset.rmsLimit) * 100).toFixed(1) }}%
              </span>
            </div>
            <div class="info-row">
              <span class="info-label">Estado</span>
              <StatusBadge :status="asset.status" />
            </div>
            <div class="info-row">
              <span class="info-label">Última actualización</span>
              <span class="info-value">{{ formatDate(asset.lastUpdate) }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Tab: Monitoreo en Vivo -->
    <div v-if="activeTab === 'live'" class="tab-content">
      <div class="charts-grid">
        <div class="chart-card full-width">
          <div class="chart-card-header">
            <h3>Forma de Onda en Tiempo Real</h3>
            <span class="live-indicator">● EN VIVO</span>
          </div>
          <WaveformChart :data="waveformData" />
        </div>

        <div class="chart-card full-width">
          <div class="chart-card-header">
            <h3>Espectro de Frecuencias (FFT)</h3>
          </div>
          <FFTChart :data="fftData" :frequencies="fftFrequencies" />
        </div>
      </div>
    </div>

    <!-- Tab: Tendencia -->
    <div v-if="activeTab === 'trend'" class="tab-content">
      <div class="chart-card">
        <div class="chart-card-header">
          <h3>Tendencia RMS Histórica</h3>
        </div>
        <TrendChart :data="trendData" :limit="asset.rmsLimit" />
      </div>
    </div>

    <!-- Tab: Alarmas -->
    <div v-if="activeTab === 'alarms'" class="tab-content">
      <div class="alarms-list">
        <div v-if="assetAlarms.length === 0" class="empty-state">
          No hay alarmas registradas para este equipo.
        </div>
        <div
          v-for="alarm in assetAlarms"
          :key="alarm.id"
          class="alarm-row"
          :class="alarm.severity"
        >
          <div class="alarm-severity-bar"></div>
          <div class="alarm-info">
            <div class="alarm-message">{{ alarm.message }}</div>
            <div class="alarm-meta">{{ formatDate(alarm.timestamp) }} · RMS: {{ alarm.rmsValue }} mm/s</div>
          </div>
          <StatusBadge :status="alarm.severity" />
        </div>
      </div>
    </div>

  </div>

  <div v-else class="not-found">
    Equipo no encontrado.
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAssetsStore } from '../stores/assetsStore.js'
import { useAlarmsStore } from '../stores/alarmsStore.js'
import StatusBadge from '../components/common/StatusBadge.vue'
import WaveformChart from '../components/charts/WaveformChart.vue'
import FFTChart from '../components/charts/FFTChart.vue'
import TrendChart from '../components/charts/TrendChart.vue'

const props = defineProps({ id: { type: String, required: true } })
const router = useRouter()
const assetsStore = useAssetsStore()
const alarmsStore = useAlarmsStore()

const asset = computed(() =>
  assetsStore.assets.find(a => a.id === Number(props.id))
)

const assetAlarms = computed(() =>
  alarmsStore.alarms.filter(a => a.assetId === Number(props.id))
)

const activeTab = ref('info')

const tabs = [
  { key: 'info',   label: '📋 Información' },
  { key: 'live',   label: '📡 Monitoreo en Vivo' },
  { key: 'trend',  label: '📈 Tendencia' },
  { key: 'alarms', label: '🚨 Alarmas' },
]

// --- Data simulada ---
const waveformData = ref([])
const fftData = ref([])
const fftFrequencies = ref([])
const trendData = ref([])

function generateWaveform() {
  const points = 200
  waveformData.value = Array.from({ length: points }, (_, i) => {
    const rms = asset.value?.rmsActual || 1
    return +(Math.sin(i * 0.15) * rms + (Math.random() - 0.5) * 0.3).toFixed(3)
  })
}

function generateFFT() {
  const bins = 64
  fftFrequencies.value = Array.from({ length: bins }, (_, i) => Math.round(i * (500 / bins)))
  fftData.value = Array.from({ length: bins }, (_, i) => {
    const rms = asset.value?.rmsActual || 1
    const base = i < 5 ? rms * 0.8 : Math.random() * rms * 0.3
    return +base.toFixed(3)
  })
}

function generateTrend() {
  const points = 20
  const now = Date.now()
  trendData.value = Array.from({ length: points }, (_, i) => {
    const rms = asset.value?.rmsActual || 1
    const variation = (Math.random() - 0.5) * rms * 0.4
    return {
      time: new Date(now - (points - i) * 60000 * 5).toLocaleTimeString('es-CO', {
        hour: '2-digit', minute: '2-digit'
      }),
      value: +(rms + variation).toFixed(2)
    }
  })
}

function formatDate(iso) {
  return new Date(iso).toLocaleString('es-CO', {
    day: '2-digit', month: '2-digit', year: 'numeric',
    hour: '2-digit', minute: '2-digit'
  })
}

let liveInterval = null

onMounted(() => {
  generateWaveform()
  generateFFT()
  generateTrend()
  // Simula actualización en tiempo real cada 2 segundos
  liveInterval = setInterval(() => {
    generateWaveform()
    generateFFT()
  }, 2000)
})

onUnmounted(() => clearInterval(liveInterval))
</script>

<style scoped>
.asset-detail {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.asset-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: var(--color-surface);
  border-radius: 12px;
  padding: 20px 24px;
  border: 1px solid var(--color-surface2);
}

.asset-header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.back-btn {
  background: var(--color-surface2);
  border: none;
  color: var(--color-text);
  padding: 8px 14px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 13px;
  transition: background 0.2s;
}

.back-btn:hover {
  background: var(--color-accent);
}

.asset-tag-title {
  font-size: 24px;
  font-weight: 700;
  color: var(--color-text);
  font-family: monospace;
}

.asset-name-title {
  font-size: 14px;
  color: var(--color-text-muted);
}

.asset-header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.rms-display {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.rms-value {
  font-size: 32px;
  font-weight: 700;
  line-height: 1;
}

.rms-unit {
  font-size: 12px;
  color: var(--color-text-muted);
}

.rms-display.normal   .rms-value { color: var(--color-normal); }
.rms-display.warning  .rms-value { color: var(--color-warning); }
.rms-display.critical .rms-value { color: var(--color-critical); }
.rms-display.offline  .rms-value { color: var(--color-offline); }

.tabs {
  display: flex;
  gap: 8px;
  border-bottom: 1px solid var(--color-surface2);
  padding-bottom: 0;
}

.tab-btn {
  background: none;
  border: none;
  color: var(--color-text-muted);
  padding: 10px 20px;
  cursor: pointer;
  font-size: 14px;
  border-bottom: 2px solid transparent;
  transition: all 0.2s;
  margin-bottom: -1px;
}

.tab-btn:hover { color: var(--color-text); }

.tab-btn.active {
  color: var(--color-text);
  border-bottom-color: var(--color-accent);
}

.tab-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* Info tab */
.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.info-card {
  background-color: var(--color-surface);
  border-radius: 12px;
  padding: 20px;
  border: 1px solid var(--color-surface2);
}

.info-card h3 {
  color: var(--color-text);
  font-size: 15px;
  margin-bottom: 16px;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--color-surface2);
}

.info-rows {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.info-label {
  font-size: 13px;
  color: var(--color-text-muted);
}

.info-value {
  font-size: 13px;
  font-weight: 600;
  color: var(--color-text);
}

.info-value.normal   { color: var(--color-normal); }
.info-value.warning  { color: var(--color-warning); }
.info-value.critical { color: var(--color-critical); }

/* Charts */
.charts-grid {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.chart-card {
  background-color: var(--color-surface);
  border-radius: 12px;
  padding: 20px;
  border: 1px solid var(--color-surface2);
}

.chart-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.chart-card-header h3 {
  color: var(--color-text);
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

/* Alarmas */
.alarms-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.alarm-row {
  display: flex;
  align-items: center;
  gap: 16px;
  background-color: var(--color-surface);
  border-radius: 10px;
  padding: 14px 16px;
  border: 1px solid var(--color-surface2);
}

.alarm-severity-bar {
  width: 4px;
  height: 40px;
  border-radius: 2px;
  flex-shrink: 0;
}

.alarm-row.warning  .alarm-severity-bar { background-color: var(--color-warning); }
.alarm-row.critical .alarm-severity-bar { background-color: var(--color-critical); }

.alarm-info { flex: 1; }

.alarm-message {
  font-size: 14px;
  color: var(--color-text);
  margin-bottom: 4px;
}

.alarm-meta {
  font-size: 12px;
  color: var(--color-text-muted);
}

.empty-state, .not-found {
  text-align: center;
  color: var(--color-text-muted);
  padding: 60px;
  font-size: 16px;
}
</style>