import { createRouter, createWebHistory } from 'vue-router'

const DashboardView = () => import('../views/DashboardView.vue')
const AlarmsView = () => import('../views/AlarmsView.vue')
const AssetDetailView = () => import('../views/AssetDetailView.vue')
const SettingsView = () => import('../views/SettingsView.vue')

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