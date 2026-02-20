import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { assetsAPI } from '../services/api.js'
import { useToast } from '../composables/useToast.js'

export const useAssetsStore = defineStore('assets', () => {
  const { success, error: showError } = useToast()
  
  const assets = ref([])
  const filterStatus = ref('all')
  const searchQuery = ref('')  
  const loading = ref(false)
  const error = ref(null)

  const filteredAssets = computed(() => {
    let result = assets.value

  
    if (searchQuery.value) {
      const query = searchQuery.value.toLowerCase()
      result = result.filter(a => 
        a.tag.toLowerCase().includes(query) ||
        a.name.toLowerCase().includes(query) ||
        (a.location && a.location.toLowerCase().includes(query))
      )
    }

    if (filterStatus.value && filterStatus.value !== 'all') {
      result = result.filter(a => a.status === filterStatus.value)
    }

    return result
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

  function setSearch(query) {
    searchQuery.value = query
  }

  async function fetchAssets() {
    loading.value = true
    error.value = null
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
      showError(`Error al cargar equipos: ${e.message}`)
    } finally {
      loading.value = false
    }
  }

  async function createAsset(assetData) {
    if (!assetData.tag || !assetData.name || !assetData.type) {
      showError('Tag, nombre y tipo son obligatorios')
      throw new Error('Tag, nombre y tipo son obligatorios')
    }

    loading.value = true
    error.value = null
    try {
      await assetsAPI.create(assetData)
      await fetchAssets()
      success('Equipo creado exitosamente')
    } catch (e) {
      error.value = e.message
      showError(`Error al crear: ${e.message}`)
      throw e
    } finally {
      loading.value = false
    }
  }

  async function updateAsset(id, data) {
    loading.value = true
    error.value = null
    try {
      await assetsAPI.update(id, data)
      
      // Actualizar localmente
      const index = assets.value.findIndex(a => a.id === id)
      if (index !== -1) {
        assets.value[index] = { ...assets.value[index], ...data }
      }
      
      success('Cambios guardados')
    } catch (e) {
      error.value = e.message
      showError(`Error al guardar: ${e.message}`)
      throw e
    } finally {
      loading.value = false
    }
  }

  async function deleteAsset(id) {
    loading.value = true
    error.value = null
    try {
      await assetsAPI.delete(id)
      await fetchAssets()
      success('Equipo eliminado')
    } catch (e) {
      error.value = e.message
      showError(`Error al eliminar: ${e.message}`)
      throw e
    } finally {
      loading.value = false
    }
  }

  return { 
    assets, 
    filteredAssets, 
    filterStatus,
    searchQuery,  
    summary, 
    loading, 
    error, 

    setFilter, 
    setSearch,  
    fetchAssets, 
    createAsset,
    updateAsset,  
    deleteAsset   
  }
})