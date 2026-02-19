<template>
  <div class="settings-section">
    <h3 class="section-title">Gestión de Equipos</h3>

    <LoadingSpinner v-if="loading" message="Cargando equipos..." />
    <ErrorState v-else-if="error" :message="error" retryable @retry="fetchAssets" />

    <template v-else>
      <div class="management-header">
        <span class="assets-count">{{ assets.length }} equipos registrados</span>
        <button class="add-btn" @click="showForm = !showForm">
          {{ showForm ? '✕ Cancelar' : '+ Agregar Equipo' }}
        </button>
      </div>

      <!-- Formulario para agregar equipo -->
      <div v-if="showForm" class="add-form">
        <h4 class="form-title">Nuevo Equipo</h4>
        <div class="form-grid">
          <div class="field-group">
            <label>Tag *</label>
            <input v-model="newAsset.tag" class="field-input" placeholder="P-101" />
          </div>
          <div class="field-group">
            <label>Nombre *</label>
            <input v-model="newAsset.name" class="field-input" placeholder="Bomba de Alimentación" />
          </div>
          <div class="field-group">
            <label>Tipo *</label>
            <select v-model="newAsset.type" class="field-input">
              <option value="">Seleccionar...</option>
              <option>Bomba Centrífuga</option>
              <option>Motor Eléctrico</option>
              <option>Compresor</option>
              <option>Ventilador</option>
              <option>Otro</option>
            </select>
          </div>
          <div class="field-group">
            <label>Ubicación</label>
            <input v-model="newAsset.location" class="field-input" placeholder="Área A - Piso 1" />
          </div>
          <div class="field-group">
            <label>RPM Nominal</label>
            <input v-model.number="newAsset.rpm_nominal" type="number" class="field-input" placeholder="1750" />
          </div>
          <div class="field-group">
            <label>Límite RMS (mm/s)</label>
            <input v-model.number="newAsset.rms_limit" type="number" class="field-input" step="0.1" placeholder="4.5" />
          </div>
        </div>
        <button class="save-btn" @click="createAsset" :disabled="saving">
          {{ saving ? 'Guardando...' : 'Guardar Equipo' }}
        </button>
      </div>

      <!-- Lista de equipos -->
      <div class="assets-list">
        <div v-for="asset in assets" :key="asset.id" class="asset-row">
          <div class="asset-row-info">
            <span class="asset-row-tag">{{ asset.tag }}</span>
            <span class="asset-row-name">{{ asset.name }}</span>
            <span class="asset-row-type">{{ asset.type }}</span>
            <span class="asset-row-location">📍 {{ asset.location }}</span>
          </div>
          <div class="asset-row-actions">
            <StatusBadge :status="asset.status" />
            <button class="delete-btn" @click="deleteAsset(asset.id)">Eliminar</button>
          </div>
        </div>
      </div>

    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { settingsAPI } from '../../services/api.js'
import StatusBadge from '../common/StatusBadge.vue'
import LoadingSpinner from '../common/LoadingSpinner.vue'
import ErrorState from '../common/ErrorState.vue'

const assets   = ref([])
const loading  = ref(false)
const saving   = ref(false)
const error    = ref(null)
const showForm = ref(false)

const newAsset = ref({
  tag: '', name: '', type: '', location: '',
  rpm_nominal: 1750, rms_limit: 4.5
})

async function fetchAssets() {
  loading.value = true
  error.value   = null
  try {
    const data   = await settingsAPI.getAssets()
    assets.value = data.map(a => ({
      id:       a.id,
      tag:      a.tag,
      name:     a.name,
      type:     a.type,
      location: a.location,
      status:   a.status
    }))
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

async function createAsset() {
  if (!newAsset.value.tag || !newAsset.value.name || !newAsset.value.type) {
    error.value = 'Tag, nombre y tipo son obligatorios'
    return
  }
  saving.value = true
  try {
    await settingsAPI.createAsset(newAsset.value)
    newAsset.value = { tag: '', name: '', type: '', location: '', rpm_nominal: 1750, rms_limit: 4.5 }
    showForm.value = false
    await fetchAssets()
  } catch (e) {
    error.value = e.message
  } finally {
    saving.value = false
  }
}

async function deleteAsset(id) {
  if (!confirm('¿Eliminar este equipo?')) return
  try {
    await settingsAPI.deleteAsset(id)
    await fetchAssets()
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

.management-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.assets-count {
  font-size: 13px;
  color: var(--color-text-muted);
}

.add-btn {
  background-color: var(--color-accent);
  border: none;
  color: white;
  padding: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 600;
  transition: opacity 0.2s;
}

.add-btn:hover { opacity: 0.85; }

.add-form {
  background-color: var(--color-surface);
  border-radius: 10px;
  padding: 20px;
  border: 1px solid var(--color-surface2);
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text-dark);
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 12px;
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

.field-input {
  background-color: var(--color-surface4);
  border: 1px solid var(--color-surface);
  border-radius: 6px;
  padding: 8px 12px;
  color: var(--color-text-dark);
  font-size: 13px;
  outline: none;
  transition: border-color 0.2s;
  width: 100%;
}

.field-input:focus { border-color: var(--color-accent); }

.save-btn {
  background-color: var(--color-accent);
  border: none;
  color: white;
  padding: 10px 24px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: opacity 0.2s;
  align-self: flex-start;
}

.save-btn:hover    { opacity: 0.85; }
.save-btn:disabled { opacity: 0.5; cursor: not-allowed; }

.assets-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.asset-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background-color: var(--color-surface);
  border-radius: 8px;
  border: 1px solid var(--color-surface2);
}

.asset-row-info {
  display: flex;
  align-items: center;
  gap: 16px;
}

.asset-row-tag {
  font-family: monospace;
  font-weight: 700;
  font-size: 14px;
  color: var(--color-text-dark);
  min-width: 60px;
}

.asset-row-name {
  font-size: 13px;
  color: var(--color-text-dark);
}

.asset-row-type, .asset-row-location {
  font-size: 12px;
  color: var(--color-text-muted);
}

.asset-row-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.delete-btn {
  background: rgba(255,68,68,0.15);
  border: none;
  color: var(--color-critical);
  padding: 6px 14px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 12px;
  font-weight: 600;
  transition: background 0.2s;
}

.delete-btn:hover { background: var(--color-critical); color: white; }
</style>