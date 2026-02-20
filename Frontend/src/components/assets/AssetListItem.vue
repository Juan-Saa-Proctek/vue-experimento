<template>
  <div class="asset-row">
    <!-- Modo Vista -->
    <template v-if="!isEditing">
      <div class="asset-row-info">
        <span class="asset-row-tag" :title="asset.tag">{{ asset.tag }}</span>
        <span class="asset-row-name" :title="asset.name">{{ asset.name }}</span>
        <span class="asset-row-type">{{ asset.type }}</span>
        <span class="asset-row-location">
          <MapPin :size="14" /> {{ asset.location }}
        </span>
      </div>
      <div class="asset-row-actions">
        <StatusBadge :status="asset.status" />
        <button class="edit-btn" @click="$emit('edit')">
          <Edit2 :size="14" />
          Editar
        </button>
        <button class="delete-btn" @click="$emit('delete')">
          Eliminar
        </button>
      </div>
    </template>

    <!-- Modo Edición -->
    <template v-else>
      <div class="edit-form">
        <div class="edit-row">
          <div class="field-group">
            <label>Tag</label>
            <input :value="editData.tag" class="field-input" disabled />
          </div>
          <div class="field-group">
            <label>Nombre *</label>
            <input 
              :value="editData.name"
              @input="updateField('name', $event.target.value)"
              class="field-input" 
            />
          </div>
          <div class="field-group">
            <label>Tipo</label>
            <select 
              :value="editData.type"
              @change="updateField('type', $event.target.value)"
              class="field-input"
            >
              <option value="">Seleccionar...</option>
              <option>Bomba Centrífuga</option>
              <option>Motor Eléctrico</option>
              <option>Compresor</option>
              <option>Ventilador</option>
              <option>Otro</option>
            </select>
          </div>
        </div>
        <div class="edit-row">
          <div class="field-group">
            <label>Ubicación</label>
            <input 
              :value="editData.location"
              @input="updateField('location', $event.target.value)"
              class="field-input" 
            />
          </div>
          <div class="field-group">
            <label>RPM Nominal</label>
            <input 
              :value="editData.rpm_nominal"
              @input="updateField('rpm_nominal', Number($event.target.value))"
              type="number" 
              class="field-input" 
            />
          </div>
          <div class="field-group">
            <label>Límite RMS</label>
            <input 
              :value="editData.rms_limit"
              @input="updateField('rms_limit', Number($event.target.value))"
              type="number" 
              step="0.1" 
              class="field-input" 
            />
          </div>
        </div>
      </div>
      <div class="edit-actions">
        <button class="save-edit-btn" @click="$emit('save')">
          <CircleCheck :size="16" />
          Guardar
        </button>
        <button class="cancel-edit-btn" @click="$emit('cancel')">
          <CircleX :size="16" />
          Cancelar
        </button>
      </div>
    </template>
  </div>
</template>

<script setup>
import { MapPin, Edit2, CircleCheck, CircleX } from 'lucide-vue-next'
import StatusBadge from '../common/StatusBadge.vue'

const props = defineProps({
  asset: { type: Object, required: true },
  isEditing: { type: Boolean, default: false },
  editData: { type: Object, default: () => ({}) }
})

const emit = defineEmits(['edit', 'delete', 'save', 'cancel', 'update:editData'])

function updateField(field, value) {
  emit('update:editData', { ...props.editData, [field]: value })
}
</script>

<style scoped>
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

.asset-row-type,
.asset-row-location {
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

.edit-btn:hover {
  opacity: 0.85;
}

.delete-btn {
  background: rgba(255, 68, 68, 0.15);
  border: none;
  color: var(--color-critical);
  padding: 6px 14px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 12px;
  font-weight: 600;
  transition: background 0.2s;
}

.delete-btn:hover {
  background: var(--color-critical);
  color: white;
}

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

.field-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
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

.field-input:focus {
  border-color: var(--color-accent);
}

.field-input:disabled {
  opacity: 0.5;
  cursor: not-allowed;
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
  transition: all 0.2s;
}

.save-edit-btn {
  background-color: var(--color-accent);
  color: white;
  border: none;
}

.save-edit-btn:hover {
  opacity: 0.85;
}

.cancel-edit-btn {
  background-color: var(--color-surface4);
  color: var(--color-text-muted);
  border: 1px solid var(--color-surface);
}

.cancel-edit-btn:hover {
  background-color: var(--color-surface3);
}
</style>