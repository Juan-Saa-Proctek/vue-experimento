<template>
  <div class="settings-view">

    <div class="settings-section">
      <h3 class="section-title">Umbrales de Alarma por Tipo de Activo</h3>
      <div class="thresholds-grid">
        <div v-for="threshold in thresholds" :key="threshold.type" class="threshold-card">
          <div class="threshold-header">
            <span class="threshold-type">{{ threshold.type }}</span>
          </div>
          <div class="threshold-fields">
            <div class="field-group">
              <label>Advertencia (mm/s)</label>
              <input
                type="number"
                v-model.number="threshold.warning"
                class="threshold-input warning"
                step="0.1"
                min="0"
              />
            </div>
            <div class="field-group">
              <label>Crítico (mm/s)</label>
              <input
                type="number"
                v-model.number="threshold.critical"
                class="threshold-input critical"
                step="0.1"
                min="0"
              />
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="settings-section">
      <h3 class="section-title">Gestión de Equipos</h3>
      <div class="assets-management">
        <div class="management-header">
          <span>{{ assetsStore.assets.length }} equipos registrados</span>
          <button class="add-btn">+ Agregar Equipo</button>
        </div>
        <div class="assets-list">
          <div
            v-for="asset in assetsStore.assets"
            :key="asset.id"
            class="asset-row"
          >
            <div class="asset-row-info">
              <span class="asset-row-tag">{{ asset.tag }}</span>
              <span class="asset-row-name">{{ asset.name }}</span>
              <span class="asset-row-type">{{ asset.type }}</span>
            </div>
            <div class="asset-row-actions">
              <StatusBadge :status="asset.status" />
              <button class="edit-btn">Editar</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="settings-section">
      <h3 class="section-title">Conexión con Backend</h3>
      <div class="connection-card">
        <div class="connection-row">
          <span class="connection-label">URL del API</span>
          <input type="text" v-model="apiUrl" class="api-input" />
        </div>
        <div class="connection-row">
          <span class="connection-label">Intervalo de actualización</span>
          <select v-model="refreshInterval" class="api-input">
            <option :value="1000">1 segundo</option>
            <option :value="2000">2 segundos</option>
            <option :value="5000">5 segundos</option>
          </select>
        </div>
        <button class="save-btn">Guardar configuración</button>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAssetsStore } from '../stores/assetsStore.js'
import StatusBadge from '../components/common/StatusBadge.vue'

const assetsStore = useAssetsStore()

const apiUrl = ref('http://localhost:8000')
const refreshInterval = ref(2000)

const thresholds = ref([
  { type: 'Bomba Centrífuga',  warning: 2.8, critical: 4.5 },
  { type: 'Motor Eléctrico',   warning: 2.8, critical: 4.5 },
  { type: 'Compresor',         warning: 3.5, critical: 5.5 },
  { type: 'Ventilador',        warning: 2.3, critical: 3.8 },
])
</script>

<style scoped>
.settings-view {
  display: flex;
  flex-direction: column;
  gap: 28px;
}

.settings-section {
  background-color: var(--color-surface4);
  border-radius: 12px;
  padding: 24px;
  border: 1px solid var(--color-surface);
}

.section-title {
  color: var(--color-text-dark);
  font-size: 15px;
  font-weight: 600;
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--color-surface2);
}

.thresholds-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 16px;
}

.threshold-card {
  background-color: var(--color-surface4);
  border-radius: 10px;
  padding: 16px;
  border: 1px solid var(--color-surface);
}

.threshold-type {
  font-size: 13px;
  font-weight: 600;
  color: var(--color-text-dark);
  display: block;
  margin-bottom: 14px;
}

.threshold-fields {
  display: flex;
  flex-direction: column;
  gap: 10px;
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
  color: var(--color-text-subtle);
  font-size: 14px;
  font-weight: 600;
  width: 100%;
  outline: none;
  transition: border-color 0.2s;
}

.threshold-input.warning:focus { border-color: var(--color-warning); }
.threshold-input.critical:focus { border-color: var(--color-critical); }

.management-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  font-size: 13px;
  color: var(--color-text-dark);
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
  background-color: var(--color-surface4);
  border-radius: 8px;
  border: 1px solid var(--color-surface);
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

.asset-row-type {
  font-size: 12px;
  color: var(--color-text-dark);
}

.asset-row-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.edit-btn {
  background: var(--color-surface2);
  border: none;
  color: var(--color-text);
  padding: 6px 14px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 12px;
  transition: background 0.2s;
}

.edit-btn:hover { background: var(--color-accent); }

.connection-card {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.connection-row {
  display: flex;
  align-items: center;
  gap: 20px;
}

.connection-label {
  font-size: 13px;
  color: var(--color-text-dark);
  min-width: 200px;
}

.api-input {
  background-color: var(--color-surface4);
  border: 1px solid var(--color-surface);
  border-radius: 8px;
  padding: 8px 14px;
  color: var(--color-text-dark);
  font-size: 13px;
  width: 300px;
  outline: none;
  transition: border-color 0.2s;
}

.api-input:focus { border-color: var(--color-accent); }

.save-btn {
  background-color: var(--color-accent);
  border: none;
  color: white;
  padding: 10px 24px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  align-self: flex-start;
  transition: opacity 0.2s;
}

.save-btn:hover { opacity: 0.85; }
</style>