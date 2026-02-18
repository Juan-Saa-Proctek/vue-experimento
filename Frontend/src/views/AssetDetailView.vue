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
        <component :is="tab.icon" v-if="tab.icon" :size="15" />
        {{ tab.label }}
      </button>
    </div>

    <!-- Tab: Info -->
    <div v-if="activeTab === 'info'" class="tab-content">
      <div class="info-grid">
        <div class="info-card">
          <h3>Datos de Placa</h3>
          <div class="info-rows">
            <AssetInfoRow label="Tag"          :value="asset.tag" />
            <AssetInfoRow label="Nombre"       :value="asset.name" />
            <AssetInfoRow label="Tipo"         :value="asset.type" />
            <AssetInfoRow label="Ubicación"    :value="asset.location" />
            <AssetInfoRow label="RPM Nominal"  :value="`${asset.rpmNominal} RPM`" />
            <AssetInfoRow label="Límite RMS"   :value="`${asset.rmsLimit} mm/s`" />
          </div>
        </div>

        <div class="info-card">
          <h3>Estado Actual</h3>
          <div class="info-rows">
            <AssetInfoRow
              label="RMS Actual"
              :value="`${asset.rmsActual.toFixed(2)} mm/s`"
              :highlight="asset.status"
            />
            <AssetInfoRow
              label="% del Límite"
              :value="`${rmsPercentage.toFixed(1)}%`"
              :highlight="asset.status"
            />
            <AssetInfoRow label="Última actualización" :value="formatDate(asset.lastUpdate)" />
          </div>
          <div class="status-row">
            <span class="info-label">Estado</span>
            <StatusBadge :status="asset.status" />
          </div>
        </div>
      </div>
    </div>

    <!-- Tab: Monitoreo en Vivo -->
    <div v-if="activeTab === 'live'" class="tab-content">
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
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAsset } from '../composables/useAsset.js'
import { useChartData } from '../composables/useChartData.js'
import { useRealtime } from '../composables/useRealtime.js'
import StatusBadge from '../components/common/StatusBadge.vue'
import AssetInfoRow from '../components/assets/AssetInfoRow.vue'
import WaveformChart from '../components/charts/WaveformChart.vue'
import FFTChart from '../components/charts/FFTChart.vue'
import TrendChart from '../components/charts/TrendChart.vue'

import { BookText, Activity, TrendingUp, BellDot } from 'lucide-vue-next';

const props = defineProps({ id: { type: String, required: true } })
const router = useRouter()

// Composables — toda la lógica vive aquí afuera
const { asset, assetAlarms, rmsPercentage, formatDate } = useAsset(props.id)
const { waveformData, fftData, fftFrequencies, trendData, initAll, refreshLive } = useChartData(asset)

// Inicia data y refresca gráficas en vivo cada 2 segundos
initAll()
useRealtime(refreshLive, 2000)

const activeTab = ref('info')

const tabs = [
  { key: 'info',   label: 'Información' , icon: BookText},
  { key: 'live',   label: 'Monitoreo en Vivo', icon: Activity },
  { key: 'trend',  label: 'Tendencia', icon: TrendingUp },
  { key: 'alarms', label: 'Alarmas', icon: BellDot },
]
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
  background-color: var(--color-surface4);
  border-radius: 12px;
  padding: 20px 24px;
  border: 1px solid var(--color-surface);
}

.asset-header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.back-btn {
  background: var(--color-surface4);
  border: 1px solid var(--color-surface);
  color: var(--color-text-dark);
  padding: 8px 14px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
  transition: all 0.2s;
  box-shadow: 0 1px 4px rgba(0,0,0,0.3);
}

.back-btn:hover {
  background: var(--color-surface3);
  box-shadow: 0 2px 8px rgba(0,0,0,0.4);
}

.asset-tag-title {
  font-size: 24px;
  font-weight: 700;
  color: var(--color-text-dark);
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
  gap: 6px;
  background-color: var(--color-surface4);
  padding: 6px;
  border-radius: 12px;
  border: 1px solid var(--color-surface);
}

.tab-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  background: none;
  border: none;
  color: var(--color-text-dark);
  padding: 8px 16px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
  border-radius: 8px;
  transition: all 0.2s;
  margin-bottom: 0; /* ← quita el margin-bottom anterior */
}

.tab-btn:hover {
  background-color: var(--color-surface3);
  color: var(--color-text-dark);
}

.tab-btn.active {
  background-color: var(--color-surface4);
  color: var(--color-text-dark);
  border-bottom: none; /* ← elimina el borde inferior anterior */
  box-shadow: 0 1px 4px rgba(0,0,0,0.3);
}

.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.info-card {
  background-color: var(--color-surface4);
  border-radius: 12px;
  padding: 20px;
  border: 1px solid var(--color-surface);
}

.info-card h3 {
  color: var(--color-text-dark);
  font-size: 15px;
  margin-bottom: 16px;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--color-surface4);
}

.info-rows {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 12px;
}

.status-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 14px;
  border-radius: 8px;
  background-color: var(--color-surfac4);
  border: 1px solid var(--color-surface);
  transition: background 0.2s;
}

.status-row:hover {
  background-color: var(--color-surface3);
}

.info-label {
  font-size: 12px;
  font-weight: 600;
  color: var(--color-text-dark);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

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

.alarms-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.alarm-row {
  display: flex;
  align-items: center;
  gap: 16px;
  background-color: var(--color-surface4);
  border-radius: 10px;
  padding: 14px 16px;
  border: 1px solid var(--color-surface);
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
  font-weight: 600;
  color: var(--color-text-dark);
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