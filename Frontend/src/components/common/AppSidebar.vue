<template>
  <aside class="sidebar" :class="{ collapsed: isCollapsed }">
    <div class="sidebar-logo">
      <LogoIcon v-if="!isCollapsed" class="logo-icon" />
      <button class="toggle-btn" @click="toggleSidebar">
        <Menu :size="20" />
      </button>
    </div>

    <nav class="sidebar-nav">
      <RouterLink to="/dashboard" class="nav-item" active-class="active">
        <Home class="nav-icon" :size="18" />
        <span class="nav-label">Dashboard</span>
      </RouterLink>

      <RouterLink to="/alarms" class="nav-item" active-class="active">
        <Bell class="nav-icon" :size="18" />
        <span class="nav-label">Alarmas</span>
        <span v-if="activeAlarms > 0 && !isCollapsed" class="alarm-badge">{{ activeAlarms }}</span>
      </RouterLink>

      <RouterLink to="/settings" class="nav-item" active-class="active">
        <Settings class="nav-icon" :size="18" />
        <span class="nav-label">Configuración</span>
      </RouterLink>
    </nav>

    <div class="sidebar-footer">
    <div class="system-status">
      <Wifi v-if="systemOnline" :size="20" color="var(--color-normal)" />
      <WifiOff v-else :size="20" color="var(--color-critical2)" />
      <span class="nav-label">{{ systemOnline ? 'Sistema En Linea' : 'Sin conexión' }}</span>
    </div>
    </div>
  </aside>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAlarmsStore } from '../../stores/alarmsStore.js'
import { Home, Bell, Settings, Wifi, WifiOff, Menu } from 'lucide-vue-next'
import LogoIcon from '@/assets/icons/logo.svg?component'

const isCollapsed = ref(false)
const alarmsStore = useAlarmsStore()
const activeAlarms = computed(() => alarmsStore.activeCount)
const systemOnline = computed(() => alarmsStore.systemOnline)

const toggleSidebar = () => {
  isCollapsed.value = !isCollapsed.value
}
</script>

<style scoped>
.sidebar {
  width: var(--sidebar-width);
  background-color: var(--color-surface);
  display: flex;
  flex-direction: column;
  border-right: 1px solid var(--color-surface2);
  flex-shrink: 0;
  transition: width 0.3s ease;  /* ← NUEVO */
  overflow: hidden;              /* ← NUEVO */
}

/* ← NUEVO: estado colapsado */
.sidebar.collapsed {
  width: 64px;
}
.sidebar-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 24px 20px;
  border-bottom: 1px solid var(--color-surface2);
}
.sidebar.collapsed .sidebar-logo {
  justify-content: center;
  padding: 24px 8px;
}
.logo-icon {
  width: 120px;
  height: auto;
  flex-shrink: 0;
  color: var(--color-text);
}
.logo-text {
  font-size: 18px;
  font-weight: 700;
  color: var(--color-text);
  letter-spacing: 1px;
}
.sidebar.collapsed .logo-text {
  display: none;
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
  color: var(--color-text);
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s;
  position: relative;
}
.sidebar.collapsed .nav-item {
  justify-content: center;
  padding: 12px;
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
  flex-shrink: 0;  
}
.nav-label {
  white-space: nowrap;
}
.sidebar.collapsed .nav-label {
  display: none;
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
.sidebar.collapsed .sidebar-footer {
  padding: 16px 8px;
  display: flex;
  justify-content: center;
}
.system-status {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: var(--color-text);
}
.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;  
}
.status-dot.online {
  background-color: var(--color-normal);
  box-shadow: 0 0 6px var(--color-normal);
}
.status-dot.offline {
  background-color: var(--color-critical2);
}
.toggle-btn {
  margin-left: auto;
  background: none;
  border: none;
  color: var(--color-text);
  cursor: pointer;
  font-size: 16px;
  padding: 4px 8px;
  border-radius: 4px;
  transition: background 0.2s;
  flex-shrink: 0;
}
.toggle-btn:hover {
  background-color: var(--color-surface2);
}
.sidebar.collapsed .toggle-btn {
  margin-left: 0;
}
</style>