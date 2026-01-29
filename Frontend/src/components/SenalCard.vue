<script setup>
import { ref } from 'vue'

// Recibimos los datos del sensor y el tipo actual desde el padre
const props = defineProps({
  valor: Number,
  estado: String,
  tipoActual: String
})

// Definimos los eventos que este componente puede disparar
const emit = defineEmits(['cambiarTipo'])

const opciones = [
  { id: 'sinusoidal', nombre: 'Onda Sinusoidal' },
  { id: 'cuadrada', nombre: 'Onda Cuadrada' },
  { id: 'triangular', nombre: 'Onda Triangular' }
]

const alCambiar = (event) => {
  // Emitimos el nuevo tipo hacia el Dashboard
  emit('cambiarTipo', event.target.value)
}
</script>

<template>
  <div class="senal-card">
    <h3>Configuración de Fuente</h3>
    
    <div class="selector-group">
      <label for="tipo">Tipo de Señal:</label>
      <select id="tipo" :value="tipoActual" @change="alCambiar">
        <option v-for="op in opciones" :key="op.id" :value="op.id">
          {{ op.nombre }}
        </option>
      </select>
    </div>

    <hr />

    <div class="info-datos">
      <div class="dato">
        <span class="label">RMS:</span>
        <span class="valor">{{ valor.toFixed(2) }} mm/s</span>
      </div>
      <div class="dato">
        <span class="label">Estado:</span>
        <span :class="['status-pill', estado.toLowerCase()]">{{ estado }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.senal-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.1);
  width: 300px;
  border-top: 5px solid #42b883;
}

.selector-group {
  margin: 15px 0;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

select {
  padding: 8px;
  border-radius: 6px;
  border: 1px solid #ddd;
  background: #f8f9fa;
  cursor: pointer;
}

.info-datos {
  margin-top: 15px;
}

.dato {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.status-pill {
  padding: 2px 10px;
  border-radius: 12px;
  font-size: 0.85em;
  font-weight: bold;
}

.normal { background: #e6ffed; color: #28a745; }
.alerta { background: #fff3e0; color: #fb8c00; }
.peligro { background: #ffebee; color: #d32f2f; }
</style>