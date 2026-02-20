<template>
  <div class="add-form">
    <h4 class="form-title">Nuevo Equipo</h4>
    <div class="form-grid">
      <div class="field-group">
        <label>Tag *</label>
        <input 
          :value="formData.tag"
          @input="updateField('tag', $event.target.value)"
          class="field-input" 
          placeholder="P-101" 
        />
      </div>
      <div class="field-group">
        <label>Nombre *</label>
        <input 
          :value="formData.name"
          @input="updateField('name', $event.target.value)"
          class="field-input" 
          placeholder="Bomba de Alimentación" 
        />
      </div>
      <div class="field-group">
        <label>Tipo *</label>
        <select 
          :value="formData.type"
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
      <div class="field-group">
        <label>Ubicación</label>
        <input 
          :value="formData.location"
          @input="updateField('location', $event.target.value)"
          class="field-input" 
          placeholder="Área A - Piso 1" 
        />
      </div>
      <div class="field-group">
        <label>RPM Nominal</label>
        <input 
          :value="formData.rpm_nominal"
          @input="updateField('rpm_nominal', Number($event.target.value))"
          type="number" 
          class="field-input" 
          placeholder="1750" 
        />
      </div>
      <div class="field-group">
        <label>Límite RMS (mm/s)</label>
        <input 
          :value="formData.rms_limit"
          @input="updateField('rms_limit', Number($event.target.value))"
          type="number" 
          class="field-input" 
          step="0.1" 
          placeholder="4.5" 
        />
      </div>
    </div>
    <button class="save-btn" @click="$emit('save')" :disabled="!isValid || saving">
      {{ saving ? 'Guardando...' : 'Guardar Equipo' }}
    </button>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  formData: { type: Object, required: true },
  saving: { type: Boolean, default: false }
})

const emit = defineEmits(['update:formData', 'save'])

const isValid = computed(() => 
  props.formData.tag && props.formData.name && props.formData.type
)

function updateField(field, value) {
  emit('update:formData', { ...props.formData, [field]: value })
}
</script>

<style scoped>
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

.field-input:focus {
  border-color: var(--color-accent);
}

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

.save-btn:hover {
  opacity: 0.85;
}

.save-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>