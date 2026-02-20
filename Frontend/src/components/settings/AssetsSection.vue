<template>
  <div class="settings-section">
    <h3 class="section-title">Gestión de Equipos</h3>

    <LoadingSpinner v-if="assetsStore.loading" message="Cargando equipos..." />
    <ErrorState v-else-if="assetsStore.error" :message="assetsStore.error" retryable @retry="assetsStore.fetchAssets" />

    <template v-else>
      <!-- Búsqueda y filtros -->
      <AssetSearchBar 
        v-model="assetsStore.searchQuery"
        v-model:filterStatus="assetsStore.filterStatus"
        @update:modelValue="pagination.resetPage()"
        @update:filterStatus="pagination.resetPage()"
      />

      <!-- Header con contador y botón -->
      <div class="management-header">
        <span class="assets-count">
          {{ assetsStore.filteredAssets.length }} equipo(s) 
          {{ assetsStore.searchQuery || assetsStore.filterStatus ? 'encontrado(s)' : 'registrados' }}
        </span>
        <button class="add-btn" @click="showForm = !showForm">
          <CircleX v-if="showForm" :size="16" />
          <CirclePlus v-else :size="16" />
          {{ showForm ? 'Cancelar' : 'Agregar Equipo' }}
        </button>
      </div>

      <!-- Formulario para agregar -->
      <AssetForm
        v-if="showForm"
        v-model:formData="newAsset"
        :saving="saving"
        @save="handleCreate"
      />

      <!-- Lista de equipos -->
      <div class="assets-list">
        <AssetListItem
          v-for="asset in pagination.paginatedItems.value"
          :key="asset.id"
          :asset="asset"
          :isEditing="editingId === asset.id"
          :editData="editForm"
          @update:editData="editForm = $event"
          @edit="startEdit(asset)"
          @cancel="cancelEdit"
          @save="handleSave"
          @delete="handleDelete(asset.id)"
        />

        <div v-if="assetsStore.filteredAssets.length === 0" class="empty-state">
          <p>No se encontraron equipos</p>
        </div>
      </div>

      <!-- Paginación -->
      <div v-if="pagination.totalPages.value > 1" class="pagination">
        <button 
          class="page-btn" 
          @click="pagination.prevPage()" 
          :disabled="pagination.currentPage.value === 1"
        >
          <CircleArrowLeft :size="16" />
        </button>
        <span class="page-info">
          Página {{ pagination.currentPage.value }} de {{ pagination.totalPages.value }}
        </span>
        <button 
          class="page-btn" 
          @click="pagination.nextPage()" 
          :disabled="pagination.currentPage.value === pagination.totalPages.value"
        >
          <CircleArrowRight :size="16" />
        </button>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, inject } from 'vue'
import { CirclePlus, CircleX, CircleArrowLeft, CircleArrowRight } from 'lucide-vue-next'
import { useAssetsStore } from '../../stores/assetsStore.js'
import { usePagination } from '../../composables/usePagination.js'
import LoadingSpinner from '../common/LoadingSpinner.vue'
import ErrorState from '../common/ErrorState.vue'
import AssetSearchBar from '../assets/AssetSearchBar.vue'
import AssetListItem from '../assets/AssetListItem.vue'
import AssetForm from '../assets/AssetForm.vue'

const confirm = inject('confirm')


const assetsStore = useAssetsStore()


const pagination = usePagination(
  computed(() => assetsStore.filteredAssets),
  5
)

// Estado local del componente
const showForm = ref(false)
const saving = ref(false)
const editingId = ref(null)
const editForm = ref({})

const newAsset = ref({
  tag: '',
  name: '',
  type: '',
  location: '',
  rpm_nominal: 1750,
  rms_limit: 4.5
})

// Handlers
async function handleCreate() {
  saving.value = true
  try {
    await assetsStore.createAsset(newAsset.value)
    newAsset.value = {
      tag: '',
      name: '',
      type: '',
      location: '',
      rpm_nominal: 1750,
      rms_limit: 4.5
    }
    showForm.value = false
  } catch (e) {
    
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

async function handleSave() {
  try {
    await assetsStore.updateAsset(editingId.value, {
      name: editForm.value.name,
      type: editForm.value.type,
      location: editForm.value.location,
      rpm_nominal: editForm.value.rpm_nominal,
      rms_limit: editForm.value.rms_limit
    })
    cancelEdit()
  } catch (e) {
    
  }
}

async function handleDelete(id) {
  const confirmed = await confirm({
    title: '¿Eliminar equipo?',
    message: 'Esta acción no se puede deshacer.',
    type: 'danger',
    confirmText: 'Sí, eliminar',
    cancelText: 'Cancelar'
  })
  
  if (!confirmed) return
  
  try {
    await assetsStore.deleteAsset(id)
  } catch (e) {
    
  }
}

onMounted(() => assetsStore.fetchAssets())
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

.add-btn:hover {
  opacity: 0.85;
}

.assets-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

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