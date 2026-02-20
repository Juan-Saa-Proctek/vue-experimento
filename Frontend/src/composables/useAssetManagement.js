// composables/useAssetManagement.js
import { ref, computed } from 'vue'
import { settingsAPI } from '../services/api.js'
import { useToast } from './useToast.js'

export function useAssetManagement() {
  const { success, error: showError } = useToast()
  const assets = ref([])
  const loading = ref(false)
  const error = ref(null)

  // Búsqueda y filtrado
  const searchQuery = ref('')
  const filterStatus = ref('')

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

    if (filterStatus.value) {
      result = result.filter(a => a.status === filterStatus.value)
    }

    return result
  })

  async function fetchAssets() {
    loading.value = true
    error.value = null
    try {
      const data = await settingsAPI.getAssets()
      assets.value = data.map(a => ({
        id: a.id,
        tag: a.tag,
        name: a.name,
        type: a.type,
        location: a.location,
        status: a.status,
        rpm_nominal: a.rpm_nominal || 0,
        rms_limit: a.rms_limit || 4.5
      }))
    } catch (e) {
      error.value = e.message
      throw e
    } finally {
      loading.value = false
    }
  }

 async function createAsset(assetData) {
    if (!assetData.tag || !assetData.name || !assetData.type) {
        showError('Tag, nombre y tipo son obligatorios') 
        throw new Error('Tag, nombre y tipo son obligatorios')
    }
    
    try {
        await settingsAPI.createAsset(assetData)
        await fetchAssets()
        success('Equipo creado exitosamente') 
    } catch (e) {
        showError(`Error al crear: ${e.message}`) 
        throw e
    }
    }

 async function updateAsset(id, data) {
    try {
        await settingsAPI.updateAsset(id, data)
        
        const index = assets.value.findIndex(a => a.id === id)
        if (index !== -1) {
        assets.value[index] = { ...assets.value[index], ...data }
        }
        
        success('Cambios guardados') 
    } catch (e) {
        showError(`Error al guardar: ${e.message}`) 
        throw e
    }
    }

 async function deleteAsset(id) {
    try {
        await settingsAPI.deleteAsset(id)
        await fetchAssets()
        success('Equipo eliminado') 
    } catch (e) {
        showError(`Error al eliminar: ${e.message}`)
        throw e
    }
    }

  return {
    // Estado
    assets,
    filteredAssets,
    loading,
    error,
    searchQuery,
    filterStatus,
    
    // Métodos
    fetchAssets,
    createAsset,
    updateAsset,
    deleteAsset
  }
}