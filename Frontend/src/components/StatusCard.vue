<script setup>
import { computed } from 'vue'

// Definimos qué datos necesita este componente para funcionar
const props = defineProps({
  valor: Number,
  estado: String,
  unidad: String
})

// Lógica de colores movida a una propiedad computada
const estiloEstado = computed(() => {
  if (props.estado === 'Normal') return { color: 'green' }
  if (props.estado === 'Alerta') return { color: 'orange' }
  if (props.estado === 'Peligro') return { color: 'red', fontWeight: 'bold' }
  return { color: 'gray' }
})
</script>

<template>
  <div class="tarjeta">
    <h2>Vibración Actual (RMS)</h2>
    <p class="valor-gigante" :style="estiloEstado">
      {{ valor }} {{ unidad }}
    </p>
    <p>Estado: {{ estado }}</p>
  </div>
</template>

<style scoped>
.tarjeta {
  border: 1px solid #ccc;
  padding: 20px;
  border-radius: 10px;
  background: #f9f9f9;
  min-width: 250px;
}
.valor-gigante {
  font-size: 3em;
  margin: 10px 0;
}
</style>