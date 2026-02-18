import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'
import AssetDetailView from '../views/AssetDetailView.vue'
import AlarmsView from '../views/AlarmsView.vue'
import SettingsView from '../views/SettingsView.vue'

const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: DashboardView
  },
  {
    path: '/asset/:id',
    name: 'AssetDetail',
    component: AssetDetailView,
    props: true
  },
  {
    path: '/alarms',
    name: 'Alarms',
    component: AlarmsView
  },
  {
    path: '/settings',
    name: 'Settings',
    component: SettingsView
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router