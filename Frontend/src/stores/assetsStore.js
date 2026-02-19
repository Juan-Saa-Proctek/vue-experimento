import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { assetsAPI } from '../services/api.js'

export const useAssetsStore = defineStore('assets', () => {
  const assets      = ref([])
  const filterStatus = ref('all')
  const loading     = ref(false)
  const error       = ref(null)

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

  async function fetchAssets() {
    loading.value = true
    error.value   = null
    try {
      const data = await assetsAPI.getAll()
      // Normalizar campos snake_case → camelCase
      assets.value = data.map(a => ({
        id:         a.id,
        tag:        a.tag,
        name:       a.name,
        type:       a.type,
        location:   a.location,
        rpmNominal: a.rpm_nominal,
        rmsLimit:   a.rms_limit,
        rmsActual:  a.rms_actual,
        status:     a.status,
        lastUpdate: a.updated_at
      }))
    } catch (e) {
      error.value = e.message
    } finally {
      loading.value = false
    }
  }

  async function createAsset(data) {
    loading.value = true
    error.value   = null
    try {
      const created = await assetsAPI.create(data)
      await fetchAssets()
      return created
    } catch (e) {
      error.value = e.message
    } finally {
      loading.value = false
    }
  }

  return { assets, filteredAssets, filterStatus, summary, loading, error, setFilter, fetchAssets, createAsset }
})