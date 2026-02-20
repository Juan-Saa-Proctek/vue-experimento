<template>
  <div class="settings-section">
    <h3 class="section-title">Gestión de Equipos</h3>

    <LoadingSpinner v-if="loading" message="Cargando equipos..." />
    <ErrorState v-else-if="error" :message="error" retryable @retry="fetchAssets" />

    <template v-else>
      <div class="search-controls">
        <div class="search-box">
          <Search :size="16" color="#000000" />
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="Buscar por tag, nombre o ubicación..."
            class="search-input"
          />
        </div>
        <select v-model="filterStatus" class="filter-select">
          <option value="">Todos los estados</option>
          <option value="normal">Normal</option>
          <option value="warning">Advertencia</option>
          <option value="critical">Crítico</option>
          <option value="offline">Desconectado</option>
        </select>
      </div>

      <div class="management-header">
        <span class="assets-count">{{ filteredAssets.length }} equipo(s) {{ searchQuery || filterStatus ? 'encontrado(s)' : 'registrados' }}</span>
        <button class="add-btn" @click="showForm = !showForm">
          <CircleX v-if="showForm" :size="16" />
          <CirclePlus v-else :size="16" />
          {{ showForm ? 'Cancelar' : 'Agregar Equipo' }}
        </button>
      </div>

      <!-- Formulario para agregar equipo -->
      <div v-if="showForm" class="add-form">
        <h4 class="form-title">Nuevo Equipo</h4>
        <div class="form-grid">
          <div class="field-group">
            <label>Tag *</label>
            <input v-model="newAsset.tag" class="field-input" placeholder="P-101" />
          </div>
          <div class="field-group">
            <label>Nombre *</label>
            <input v-model="newAsset.name" class="field-input" placeholder="Bomba de Alimentación" />
          </div>
          <div class="field-group">
            <label>Tipo *</label>
            <select v-model="newAsset.type" class="field-input">
              <option value="">Seleccionar...</option>
              <option>Bomba Centrífuga</option>
              <option>Motor Eléctrico</option>
              <option>Compresor</option>
              <option>Ventilador</option>
              <option>Otro</option>
            </select>
          </div>
          <div class="field-group">
            <label>Ubicación</label>
            <input v-model="newAsset.location" class="field-input" placeholder="Área A - Piso 1" />
          </div>
          <div class="field-group">
            <label>RPM Nominal</label>
            <input v-model.number="newAsset.rpm_nominal" type="number" class="field-input" placeholder="1750" />
          </div>
          <div class="field-group">
            <label>Límite RMS (mm/s)</label>
            <input v-model.number="newAsset.rms_limit" type="number" class="field-input" step="0.1" placeholder="4.5" />
          </div>
        </div>
        <button class="save-btn" @click="createAsset" :disabled="saving">
          {{ saving ? 'Guardando...' : 'Guardar Equipo' }}
        </button>
      </div>

      <!-- Lista de equipos con paginación -->
      <div class="assets-list">
        <div v-for="asset in paginatedAssets" :key="asset.id" class="asset-row">
          <template v-if="editingId !== asset.id">
            <div class="asset-row-info">
              <span class="asset-row-tag" :title="asset.tag">{{ asset.tag }}</span>
              <span class="asset-row-name" :title="asset.name">{{ asset.name }}</span>
              <span class="asset-row-type">{{ asset.type }}</span>
              <span class="asset-row-location"><MapPin :size="14" /> {{ asset.location }}</span>
            </div>
            <div class="asset-row-actions">
              <StatusBadge :status="asset.status" />
              <button class="edit-btn" @click="startEdit(asset)">
                <Edit2 :size="14" />
                Editar
              </button>
              <button class="delete-btn" @click="deleteAsset(asset.id)">Eliminar</button>
            </div>
          </template>

          <!-- Modo Edición -->
          <template v-else>
            <div class="edit-form">
              <div class="edit-row">
                <div class="field-group">
                  <label>Tag</label>
                  <input v-model="editForm.tag" class="field-input" disabled />
                </div>
                <div class="field-group">
                  <label>Nombre *</label>
                  <input v-model="editForm.name" class="field-input" />
                </div>
                <div class="field-group">
                  <label>Tipo</label>
                  <input v-model="editForm.type" class="field-input" />
                </div>
              </div>
              <div class="edit-row">
                <div class="field-group">
                  <label>Ubicación</label>
                  <input v-model="editForm.location" class="field-input" />
                </div>
                <div class="field-group">
                  <label>RPM Nominal</label>
                  <input v-model.number="editForm.rpm_nominal" type="number" class="field-input" />
                </div>
                <div class="field-group">
                  <label>Límite RMS</label>
                  <input v-model.number="editForm.rms_limit" type="number" step="0.1" class="field-input" />
                </div>
              </div>
            </div>
            <div class="edit-actions">
              <button class="save-edit-btn" @click="saveEdit">
                <CircleCheck :size="16" />
                Guardar
              </button>
              <button class="cancel-edit-btn" @click="cancelEdit">
                <CircleX :size="16" />
                Cancelar
              </button>
            </div>
          </template>
        </div>

   
        <div v-if="filteredAssets.length === 0" class="empty-state">
          <p>No se encontraron equipos</p>
        </div>
      </div>


      <div v-if="totalPages > 1" class="pagination">
        <button class="page-btn" @click="currentPage--" :disabled="currentPage === 1">
          <CircleArrowLeft :size="16" />
        </button>
        <span class="page-info">Página {{ currentPage }} de {{ totalPages }}</span>
        <button class="page-btn" @click="currentPage++" :disabled="currentPage === totalPages">
          <CircleArrowRight :size="16" />
        </button>
      </div>

    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { settingsAPI } from '../../services/api.js'
import StatusBadge from '../common/StatusBadge.vue'
import LoadingSpinner from '../common/LoadingSpinner.vue'
import ErrorState from '../common/ErrorState.vue'
import { CirclePlus, CircleX, MapPin, Search, Edit2, CircleArrowLeft, CircleArrowRight,CircleCheck } from 'lucide-vue-next'

const assets   = ref([])
const loading  = ref(false)
const saving   = ref(false)
const error    = ref(null)
const showForm = ref(false)


const searchQuery = ref('')
const filterStatus = ref('')
const currentPage = ref(1)
const itemsPerPage = 5
const editingId = ref(null)
const editForm = ref({})

const newAsset = ref({
  tag: '', name: '', type: '', location: '',
  rpm_nominal: 1750, rms_limit: 4.5
})


const filteredAssets = computed(() => {
  let result = assets.value

  // Filtro de búsqueda
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(a => 
      a.tag.toLowerCase().includes(query) ||
      a.name.toLowerCase().includes(query) ||
      (a.location && a.location.toLowerCase().includes(query))
    )
  }

  // Filtro de estado
  if (filterStatus.value) {
    result = result.filter(a => a.status === filterStatus.value)
  }

  return result
})

const totalPages = computed(() => 
  Math.ceil(filteredAssets.value.length / itemsPerPage)
)

const paginatedAssets = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredAssets.value.slice(start, end)
})

async function fetchAssets() {
  loading.value = true
  error.value   = null
  try {
    const data   = await settingsAPI.getAssets()
    assets.value = data.map(a => ({
      id:       a.id,
      tag:      a.tag,
      name:     a.name,
      type:     a.type,
      location: a.location,
      status:   a.status,
      rpm_nominal: a.rpm_nominal || 0,
      rms_limit: a.rms_limit || 4.5
    }))
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

async function createAsset() {
  if (!newAsset.value.tag || !newAsset.value.name || !newAsset.value.type) {
    error.value = 'Tag, nombre y tipo son obligatorios'
    return
  }
  saving.value = true
  try {
    await settingsAPI.createAsset(newAsset.value)
    newAsset.value = { tag: '', name: '', type: '', location: '', rpm_nominal: 1750, rms_limit: 4.5 }
    showForm.value = false
    await fetchAssets()
  } catch (e) {
    error.value = e.message
  } finally {
    saving.value = false
  }
}

function startEdit(asset) {
  editingId.value = asset.id
  editForm.value = { ...asset }
}

function cancelEdit() {
  editingId.value = null
  editForm.value = {}
}

async function saveEdit() {
  try {
    await settingsAPI.updateAsset(editingId.value, {
      name: editForm.value.name,
      type: editForm.value.type,
      location: editForm.value.location,
      rpm_nominal: editForm.value.rpm_nominal,
      rms_limit: editForm.value.rms_limit
    })
    
    const index = assets.value.findIndex(a => a.id === editingId.value)
    if (index !== -1) {
      assets.value[index] = { ...editForm.value }
    }
    
    editingId.value = null
    editForm.value = {}
  } catch (e) {
    error.value = e.message
  }
}

async function deleteAsset(id) {
  if (!confirm('¿Eliminar este equipo?')) return
  try {
    await settingsAPI.deleteAsset(id)
    await fetchAssets()
  } catch (e) {
    error.value = e.message
  }
}

onMounted(() => fetchAssets())
</script>

<style scoped>
.settings-section {
  background-color: var(--color-surface4);
  border-radius: 12px;
  padding: 24px;
  border: 1px solid var(--color-surface);
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.section-title {
  color: var(--color-text-dark);
  font-size: 15px;
  font-weight: 600;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--color-surface2);
}

.search-controls {
  display: flex;
  gap: 12px;
  align-items: center;
}

.search-box {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background-color: var(--color-surface4);
  border: 1px solid var(--color-surface);
  border-radius: 8px;
}

.search-input {
  flex: 1;
  background: transparent;
  border: none;
  color: var(--color-text-dark);
  font-size: 13px;
  outline: none;
}

.filter-select {
  padding: 8px 12px;
  background-color: var(--color-surface4);
  border: 1px solid var(--color-surface);
  border-radius: 8px;
  color: var(--color-text-dark);
  font-size: 13px;
  outline: none;
}

.management-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.assets-count {
  font-size: 13px;
  color: var(--color-text-muted);
}

.add-btn {
  display: flex;
  align-items: center;
  gap: 6px;
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

.add-btn:hover { opacity: 0.85; }

.add-form {
  background-color: var(--color-surface3);
  border-radius: 10px;
  padding: 20px;
  border: 1px solid var(--color-surface);
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text-dark);
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 12px;
}

.field-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.field-group label {
  font-size: 11px;
  color: var(--color-text-muted);
  text-transform: uppercase;
}

.field-input {
  background-color: var(--color-surface4);
  border: 1px solid var(--color-surface);
  border-radius: 6px;
  padding: 8px 12px;
  color: var(--color-text-dark);
  font-size: 13px;
  outline: none;
  transition: border-color 0.2s;
  width: 100%;
}

.field-input:focus { border-color: var(--color-accent); }
.field-input:disabled { opacity: 0.5; cursor: not-allowed; }

.save-btn {
  background-color: var(--color-accent);
  border: none;
  color: white;
  padding: 10px 24px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: opacity 0.2s;
  align-self: flex-start;
}

.save-btn:hover    { opacity: 0.85; }
.save-btn:disabled { opacity: 0.5; cursor: not-allowed; }

.assets-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.asset-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background-color: var(--color-surface3);
  border-radius: 8px;
  border: 1px solid var(--color-surface);
}

.asset-row-info {
  display: flex;
  align-items: center;
  gap: 16px;
  flex: 1;
  min-width: 0; 
}

.asset-row-tag {
  font-family: monospace;
  font-weight: 700;
  font-size: 14px;
  color: var(--color-text-dark);
  min-width: 80px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.asset-row-name {
  font-size: 13px;
  color: var(--color-text-dark);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 200px;
}

.asset-row-type, .asset-row-location {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: var(--color-text-muted);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.asset-row-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}


.edit-btn {
  display: flex;
  align-items: center;
  gap: 6px;
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

.edit-btn:hover { opacity: 0.85; }

.delete-btn {
  background: rgba(255,68,68,0.15);
  border: none;
  color: var(--color-critical);
  padding: 6px 14px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 12px;
  font-weight: 600;
  transition: background 0.2s;
}

.delete-btn:hover { background: var(--color-critical); color: white; }


.edit-form {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.edit-row {
  display: flex;
  gap: 12px;
}

.edit-actions {
  display: flex;
  gap: 8px;
}

.save-edit-btn,
.cancel-edit-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 6px 14px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 12px;
  font-weight: 600;
  transition: opacity 0.2s;
  border: none;
}

.save-edit-btn {
  background-color: var(--color-accent);
  color: white;
}

.save-edit-btn:hover { opacity: 0.85; }

.cancel-edit-btn {
  background-color: var(--color-accent);
  color: white;
}

.cancel-edit-btn:hover  { opacity: 0.85; }


.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  padding: 12px 0;
  border-top: 1px solid var(--color-surface2);
}

.page-btn {
  display: flex;
  align-items: center;
  padding: 6px 10px;
  background-color: var(--color-surface4);
  border: 1px solid var(--color-surface);
  border-radius: 6px;
  color: var(--color-text-dark);
  cursor: pointer;
  transition: all 0.2s;
}

.page-btn:hover:not(:disabled) {
  background-color: var(--color-surface3);
  border-color: var(--color-accent);
}

.page-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.page-info {
  font-size: 13px;
  color: var(--color-text-muted);
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: var(--color-text-muted);
  font-size: 13px;
}
</style>