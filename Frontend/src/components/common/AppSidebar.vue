<template>
  <aside class="sidebar">
    <div class="sidebar-logo">
      <span class="logo-icon">⚙️</span>
      <span class="logo-text">VibMonitor</span>
    </div>

    <nav class="sidebar-nav">
      <RouterLink to="/dashboard" class="nav-item" active-class="active">
        <span class="nav-icon">🏠</span>
        <span>Dashboard</span>
      </RouterLink>

      <RouterLink to="/alarms" class="nav-item" active-class="active">
        <span class="nav-icon">🚨</span>
        <span>Alarmas</span>
        <span v-if="activeAlarms > 0" class="alarm-badge">{{ activeAlarms }}</span>
      </RouterLink>

      <RouterLink to="/settings" class="nav-item" active-class="active">
        <span class="nav-icon">⚙️</span>
        <span>Configuración</span>
      </RouterLink>
    </nav>

    <div class="sidebar-footer">
      <div class="system-status">
        <span class="status-dot" :class="systemOnline ? 'online' : 'offline'"></span>
        <span>{{ systemOnline ? 'Sistema Online' : 'Sin conexión' }}</span>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { computed } from 'vue'
import { useAlarmsStore } from '../../stores/alarmsStore.js'

const alarmsStore = useAlarmsStore()
const activeAlarms = computed(() => alarmsStore.activeCount)
const systemOnline = computed(() => alarmsStore.systemOnline)
</script>

<style scoped>
.sidebar {
  width: var(--sidebar-width);
  background-color: var(--color-surface);
  display: flex;
  flex-direction: column;
  border-right: 1px solid var(--color-surface2);
  flex-shrink: 0;
}

.sidebar-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 24px 20px;
  border-bottom: 1px solid var(--color-surface2);
}

.logo-icon {
  font-size: 24px;
}

.logo-text {
  font-size: 18px;
  font-weight: 700;
  color: var(--color-accent);
  letter-spacing: 1px;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 16px 12px;
  flex: 1;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: 8px;
  color: var(--color-text-muted);
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s;
  position: relative;
}

.nav-item:hover {
  background-color: var(--color-surface2);
  color: var(--color-text);
}

.nav-item.active {
  background-color: var(--color-surface2);
  color: var(--color-text);
  border-left: 3px solid var(--color-accent);
}

.nav-icon {
  font-size: 18px;
}

.alarm-badge {
  margin-left: auto;
  background-color: var(--color-critical);
  color: white;
  font-size: 11px;
  font-weight: 700;
  padding: 2px 7px;
  border-radius: 10px;
}

.sidebar-footer {
  padding: 16px 20px;
  border-top: 1px solid var(--color-surface2);
}

.system-status {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: var(--color-text-muted);
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.status-dot.online {
  background-color: var(--color-normal);
  box-shadow: 0 0 6px var(--color-normal);
}

.status-dot.offline {
  background-color: var(--color-offline);
}
</style>