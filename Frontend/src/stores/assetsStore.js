import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { mockAssets } from '../mock/assets.mock.js'

export const useAssetsStore = defineStore('assets', () => {
  const assets = ref([...mockAssets])
  const filterStatus = ref('all')
  const loading = ref(false)
  const error = ref(null)

  const filteredAssets = computed(() => {
    if (filterStatus.value === 'all') return assets.value
    return assets.value.filter(a => a.status === filterStatus.value)
  })

  const summary = computed(() => ({
    total:    assets.value.length,
    normal:   assets.value.filter(a => a.status === 'normal').length,
    warning:  assets.value.filter(a => a.status === 'warning').length,
    critical: assets.value.filter(a => a.status === 'critical').length,
    offline:  assets.value.filter(a => a.status === 'offline').length,
  }))

  function setFilter(status) {
    filterStatus.value = status
  }

  // Cuando conectes el backend, esta función llama a la API
  // y reemplaza el mock. El resto de la app no cambia nada.
  async function fetchAssets() {
    loading.value = true
    error.value = null
    try {
      // TODO: reemplazar por llamada real
      // const data = await api.getAssets()
      // assets.value = data
      assets.value = [...mockAssets]
    } catch (e) {
      error.value = 'No se pudieron cargar los equipos'
    } finally {
      loading.value = false
    }
  }

  return { assets, filteredAssets, filterStatus, summary, loading, error, setFilter, fetchAssets }
})