<template>
  <div class="settings-section">
    <h3 class="section-title">Estado del Sistema</h3>

    <div class="status-grid" v-if="status">
      <div class="status-card">
        <span class="status-number">{{ status.total_assets }}</span>
        <span class="status-label">Equipos registrados</span>
      </div>
      <div class="status-card online">
        <span class="status-number">{{ status.online_assets }}</span>
        <span class="status-label">En línea</span>
      </div>
      <div class="status-card critical">
        <span class="status-number">{{ status.critical_assets }}</span>
        <span class="status-label">Críticos</span>
      </div>
    </div>

    <div class="connection-card">
      <h4 class="subsection-title">Conexión con Backend</h4>
      <div class="connection-row">
        <span class="connection-label">URL del API</span>
        <input type="text" v-model="apiUrl" class="api-input" placeholder="http://localhost:8000" />
      </div>
      <div class="connection-row">
        <span class="connection-label">Intervalo de actualización</span>
        <select v-model="refreshInterval" class="api-input">
          <option :value="1000">1 segundo</option>
          <option :value="2000">2 segundos</option>
          <option :value="5000">5 segundos</option>
        </select>
      </div>
      <div class="connection-row">
        <span class="connection-label">Estado de conexión</span>
        <span class="connection-status" :class="isOnline ? 'online' : 'offline'">
          {{ isOnline ? '● Conectado' : '● Desconectado' }}
        </span>
      </div>
      <button class="save-btn" @click="testConnection">Probar conexión</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { settingsAPI } from '../../services/api.js'

const status          = ref(null)
const apiUrl          = ref('http://localhost:8000')
const refreshInterval = ref(2000)
const isOnline        = ref(false)

async function fetchStatus() {
  try {
    status.value  = await settingsAPI.getStatus()
    isOnline.value = true
  } catch {
    isOnline.value = false
  }
}

async function testConnection() {
  await fetchStatus()
}

onMounted(() => fetchStatus())
</script>

<style scoped>
.settings-section {
  background-color: var(--color-surface4);
  border-radius: 12px;
  padding: 24px;
  border: 1px solid var(--color-surface);
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.section-title {
  color: var(--color-text-dark);
  font-size: 15px;
  font-weight: 600;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--color-surface2);
}

.subsection-title {
  color: var(--color-text-dark);
  font-size: 13px;
  font-weight: 600;
  margin-bottom: 12px;
}

.status-grid {
  display: flex;
  gap: 12px;
}

.status-card {
  background-color: var(--color-surface3);
  border-radius: 10px;
  padding: 16px 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  border: 1px solid var(--color-surface);
  min-width: 120px;
}

.status-card.online   { border-top: 3px solid var(--color-normal); }
.status-card.critical { border-top: 3px solid var(--color-critical); }

.status-number {
  font-size: 32px;
  font-weight: 700;
  color: var(--color-text-dark);
}

.status-card.online   .status-number { color: var(--color-normal); }
.status-card.critical .status-number { color: var(--color-critical); }

.status-label {
  font-size: 12px;
  color: var(--color-text-muted);
  text-transform: uppercase;
}

.connection-card {
  background-color: var(--color-surface3);
  border-radius: 10px;
  padding: 20px;
  border: 1px solid var(--color-surface);
}

.connection-row {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 12px;
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

.connection-status {
  font-size: 13px;
  font-weight: 600;
}

.connection-status.online  { color: var(--color-normal); }
.connection-status.offline { color: var(--color-critical); }

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
  margin-top: 8px;
}

.save-btn:hover { opacity: 0.85; }
</style>