<template>
  <header class="header">
    <div class="header-left">
      <h1 class="page-title">{{ pageTitle }}</h1>
    </div>

    <div class="header-right">
      <div class="clock">{{ currentTime }}</div>
      <div class="divider"></div>
      <div class="alarms-indicator" :class="{ 'has-alarms': activeAlarms > 0 }">
        🚨 {{ activeAlarms }} alarma{{ activeAlarms !== 1 ? 's' : '' }} activa{{ activeAlarms !== 1 ? 's' : '' }}
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAlarmsStore } from '../../stores/alarmsStore.js'

const route = useRoute()
const alarmsStore = useAlarmsStore()
const activeAlarms = computed(() => alarmsStore.activeCount)

const pageTitles = {
  Dashboard: 'Dashboard General',
  AssetDetail: 'Detalle del Activo',
  Alarms: 'Centro de Alarmas',
  Settings: 'Configuración'
}

const pageTitle = computed(() => pageTitles[route.name] || 'VibMonitor')

const currentTime = ref('')
let timer = null

function updateTime() {
  const now = new Date()
  currentTime.value = now.toLocaleString('es-CO', {
    day: '2-digit', month: '2-digit', year: 'numeric',
    hour: '2-digit', minute: '2-digit', second: '2-digit'
  })
}

onMounted(() => {
  updateTime()
  timer = setInterval(updateTime, 1000)
})

onUnmounted(() => clearInterval(timer))
</script>

<style scoped>
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  height: 60px;
  background-color: var(--color-surface);
  border-bottom: 1px solid var(--color-surface2);
  flex-shrink: 0;
}

.page-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--color-text);
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.clock {
  font-size: 13px;
  color: var(--color-text-muted);
  font-family: monospace;
}

.divider {
  width: 1px;
  height: 24px;
  background-color: var(--color-surface2);
}

.alarms-indicator {
  font-size: 13px;
  color: var(--color-text-muted);
  padding: 4px 12px;
  border-radius: 20px;
  background-color: var(--color-surface2);
}

.alarms-indicator.has-alarms {
  color: var(--color-critical);
  background-color: rgba(255, 68, 68, 0.15);
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}
</style>