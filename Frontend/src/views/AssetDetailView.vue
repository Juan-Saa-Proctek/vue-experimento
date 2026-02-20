<template>
  <div class="asset-detail">
    <LoadingSpinner v-if="assetsStore.loading" message="Cargando activo..." />
    <ErrorState
      v-else-if="assetsStore.error"
      :message="assetsStore.error"
      retryable
      @retry="assetsStore.fetchAssets"
    />
    <template v-else-if="asset">

      <!-- Header del activo -->
      <div class="asset-header">
        <div class="asset-header-left">
          <button class="back-btn" @click="router.back()">
            <CircleArrowLeft size="16" />
            Volver
          </button>
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

      <!-- Contenido de tabs -->
      <AssetInfoTab
        v-if="activeTab === 'info'"
        :asset="asset"
        :rmsPercentage="rmsPercentage"
        :formatDate="formatDate"
      />
      <AssetLiveTab
        v-if="activeTab === 'live'"
        :asset="asset"
        :waveformData="waveformData"
        :fftData="fftData"
        :fftFrequencies="fftFrequencies"
      />
      <AssetTrendTab
        v-if="activeTab === 'trend'"
        :trendData="trendData"
        :rmsLimit="asset.rmsLimit"
        @point-click="onTrendPointClick"
      />
      <AssetAlarmsTab
        v-if="activeTab === 'alarms'"
        :alarms="assetAlarms"
        :formatDate="formatDate"
      />

      <!-- Modal FFT histórica -->
      <FFTModal
        v-if="showFFTModal"
        :time="modalPoint?.time"
        :value="modalPoint?.value"
        :fftData="modalPoint?.fftData"
        :frequencies="modalPoint?.frequencies"
        :rpmNominal="asset.rpmNominal"
        @close="showFFTModal = false"
      />

    </template>
    <ErrorState v-else message="Equipo no encontrado." />
  </div>
</template>

<script setup>
  import { ref, onUnmounted } from 'vue'
  import { useRouter } from 'vue-router'
  import { useAssetsStore } from '../stores/assetsStore.js'
  import { useAsset } from '../composables/useAsset.js'
  import { useChartData } from '../composables/useChartData.js'
  import { useRealtime } from '../composables/useRealtime.js'
  import { BookText, Activity, TrendingUp, BellDot, CircleArrowLeft } from 'lucide-vue-next'
  import StatusBadge    from '../components/common/StatusBadge.vue'
  import LoadingSpinner from '../components/common/LoadingSpinner.vue'
  import ErrorState     from '../components/common/ErrorState.vue'
  import AssetInfoTab   from '../components/assets/AssetInfoTab.vue'
  import AssetLiveTab   from '../components/assets/AssetLiveTab.vue'
  import AssetTrendTab  from '../components/assets/AssetTrendTab.vue'
  import AssetAlarmsTab from '../components/assets/AssetAlarmsTab.vue'
  import FFTModal       from '../components/common/FFTModal.vue'

  const props = defineProps({ id: { type: String, required: true } })
  const router = useRouter()
  const assetsStore = useAssetsStore()

  const { asset, assetAlarms, rmsPercentage, formatDate } = useAsset(props.id)
  const {
    waveformData, fftData, fftFrequencies, trendData,
    initAll, refreshLive, disconnectWebSocket,
    fetchHistoricalFFT,   // ← NUEVO
  } = useChartData(asset)

  initAll(Number(props.id))
  useRealtime(refreshLive, 2000)
  onUnmounted(() => disconnectWebSocket())

  const activeTab = ref('info')
  const tabs = [
    { key: 'info',   label: 'Información',      icon: BookText  },
    { key: 'live',   label: 'Monitoreo en Vivo', icon: Activity  },
    { key: 'trend',  label: 'Tendencia',          icon: TrendingUp },
    { key: 'alarms', label: 'Alarmas',            icon: BellDot  },
  ]

  const showFFTModal = ref(false)
  const modalPoint   = ref(null)

  async function onTrendPointClick({ time, value, timestamp }) {  
   
    const historical = await fetchHistoricalFFT(Number(props.id), timestamp)

    modalPoint.value = {
      time,
      value,
      fftData: historical.fftData,
      frequencies: historical.frequencies,
    }
    showFFTModal.value = true
  }
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
  display: flex;
  align-items: center;
  gap: 6px;
  background: var(--color-accent);
  border: none;
  color: white;
  padding: 8px 14px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
  transition: all 0.2s;
  box-shadow: 0 1px 4px rgba(0,0,0,0.3);
}

.back-btn:hover {
  opacity: 0.85;
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
  margin-bottom: 0;
}

.tab-btn:hover {
  background-color: var(--color-surface3);
  color: var(--color-text-dark);
}

.tab-btn.active {
  background-color: var(--color-surface3);
  color: var(--color-text-dark);
  border-bottom: none;
  box-shadow: 0 1px 4px rgba(0,0,0,0.3);
}
</style>