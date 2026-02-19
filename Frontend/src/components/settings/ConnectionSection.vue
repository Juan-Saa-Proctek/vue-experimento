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

    <div class="connection-row">
      <span class="connection-status" :class="isOnline ? 'online' : 'offline'">
        {{ isOnline ? '● Servidor conectado' : '● Servidor desconectado' }}
      </span>
      <button class="save-btn" @click="fetchStatus">Actualizar</button>
    </div>

    <div class="connection-card">
      <h4 class="subsection-title">Importar Activos desde PCH</h4>
      <p class="pch-description">
        Conecta con un servidor PCH Engineering para importar automáticamente
        los activos industriales a este sistema.
      </p>
      <button class="pch-btn" @click="showPCHModal = true">
        <Server :size="15" />
        Conectar servidor PCH
      </button>
    </div>

    <PCHSyncModal
      :show="showPCHModal"
      @close="showPCHModal = false"
      @synced="onPCHSynced"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Server } from 'lucide-vue-next'
import { settingsAPI } from '../../services/api.js'
import PCHSyncModal from './PCHSyncModal.vue'

const status       = ref(null)
const isOnline     = ref(false)
const showPCHModal = ref(false)

async function fetchStatus() {
  try {
    status.value   = await settingsAPI.getStatus()
    isOnline.value = true
  } catch {
    isOnline.value = false
  }
}

function onPCHSynced() {
  fetchStatus()
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

.connection-row {
  display: flex;
  align-items: center;
  gap: 16px;
}

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
  padding: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 600;
  transition: opacity 0.2s;
}
.save-btn:hover { opacity: 0.85; }

.connection-card {
  background-color: var(--color-surface3);
  border-radius: 10px;
  padding: 20px;
  border: 1px solid var(--color-surface);
}

.pch-description {
  font-size: 13px;
  color: var(--color-text-muted);
  margin-bottom: 14px;
  line-height: 1.5;
}

.pch-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  background-color: var(--color-accent);
  border: none;
  color: white;
  padding: 10px 20px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: opacity 0.2s;
}
.pch-btn:hover { opacity: 0.85; }
</style>