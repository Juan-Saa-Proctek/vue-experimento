<template>
  <div class="settings-section">
    <h3 class="section-title">Umbrales de Alarma por Equipo</h3>

    <LoadingSpinner v-if="loading" message="Cargando equipos..." />
    <ErrorState v-else-if="error" :message="error" retryable @retry="fetchAssets" />

    <template v-else>
      <div class="thresholds-grid">
        <div v-for="asset in assets" :key="asset.id" class="threshold-card">
          <div class="threshold-header">
            <span class="threshold-tag">{{ asset.tag }}</span>
            <span class="threshold-type">{{ asset.type }}</span>
          </div>
          <div class="threshold-fields">
            <div class="field-group">
              <label>Límite RMS (mm/s)</label>
              <input
                type="number"
                v-model.number="asset.rmsLimit"
                class="threshold-input"
                step="0.1"
                min="0"
              />
            </div>
          </div>
          <button class="apply-btn" @click="applyThreshold(asset)">
            Aplicar
          </button>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { settingsAPI } from '../../services/api.js'
import LoadingSpinner from '../common/LoadingSpinner.vue'
import ErrorState from '../common/ErrorState.vue'

const assets  = ref([])
const loading = ref(false)
const error   = ref(null)

async function fetchAssets() {
  loading.value = true
  error.value   = null
  try {
    const data  = await settingsAPI.getAssets()
    assets.value = data.map(a => ({
      id:       a.id,
      tag:      a.tag,
      name:     a.name,
      type:     a.type,
      rmsLimit: a.rms_limit
    }))
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

async function applyThreshold(asset) {
  try {
    await settingsAPI.updateThreshold(asset.id, asset.rmsLimit)
  } catch (e) {
    error.value = e.message
  }
}

onMounted(() => fetchAssets())
</script>

<style scoped>
.settings-section {
  background-color: var(--color-surface4);
  border-radius: 12px;
  padding: 24px;
  border: 1px solid var(--color-surface);
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.section-title {
  color: var(--color-text-dark);
  font-size: 15px;
  font-weight: 600;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--color-surface2);
}

.thresholds-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
}

.threshold-card {
  background-color: var(--color-surface3);
  border-radius: 10px;
  padding: 16px;
  border: 1px solid var(--color-surface);
  display: flex;
  flex-direction: column;
  gap: 12px;
  overflow: hidden;
  max-width: 100%;
  min-width: 0; 
}

.threshold-header {
  display: flex;
  flex-direction: column;
  gap: 2px;
  overflow: hidden;
}

.threshold-tag {
  font-family: monospace;
  font-weight: 700;
  font-size: 16px;
  color: var(--color-text-dark);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.threshold-type {
  font-size: 11px;
  font-weight: 600;
  color: var(--color-text-dark);
  text-transform: uppercase;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.field-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.field-group label {
  font-size: 11px;
  color: var(--color-text-muted);
  text-transform: uppercase;
}

.threshold-input {
  background-color: var(--color-surface4);
  border: 1px solid var(--color-surface);
  border-radius: 6px;
  padding: 8px 12px;
  color: var(--color-text-dark);
  font-size: 14px;
  font-weight: 600;
  width: 100%;
  outline: none;
  transition: border-color 0.2s;
}

.threshold-input:focus { border-color: var(--color-warning); }

.apply-btn {
  background-color: var(--color-accent);
  border: none;
  color: white;
  padding: 8px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 12px;
  font-weight: 600;
  transition: background 0.2s;
}

.apply-btn:hover { opacity: 0.85; }
</style>