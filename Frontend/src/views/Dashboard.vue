<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { sensorService} from '../services/sensorServices'
import StatusCard from '../components/StatusCard.vue'
import GraficaCard from '../components/GraficaCard.vue'
import SenalCard from '../components/SenalCard.vue'
import SenalGraficaCard from '../components/SenalGraficaCard.vue'

const datosSensor = ref({ valor: 0, estado: 'Cargando...', unidad: 'mm/s' })
let intervalo = null

const tipoDeOnda = ref('sinusoidal') // Estado inicial
const datos = ref({ valor: 0, estado: 'Normal', datos_onda: []})
let timer = null

const fetchDatos = async () => {
  try {
    // Llamamos a la API pasando el tipo de onda actual
    const res = await sensorService.getSenal(tipoDeOnda.value)
    datos.value = res
  } catch (error) {
    console.error("Error:", error)
  }
}

// Función que se ejecuta cuando el hijo emite 'cambiarTipo'
const handleCambioTipo = (nuevoTipo) => {
  tipoDeOnda.value = nuevoTipo
  fetchDatos() // Actualizamos inmediatamente
}

// Color dinámico según el estado
const colorActual = computed(() => {
  if (datosSensor.value.estado === 'Normal') return '#42b883' // Verde
  if (datosSensor.value.estado === 'Alerta') return '#f39c12' // Naranja
  return '#e74c3c' // Rojo
})

const actualizar = async () => {
  try {
    const data = await sensorService.getVibracion()
    datosSensor.value = data
  } catch (e) {
    datosSensor.value.estado = 'Desconectado'
  }
}

onMounted(() => {
  intervalo = setInterval(actualizar, 1000)
})

onUnmounted(() => clearInterval(intervalo))
</script>

<template>
  <div class="dashboard">
    <h1>Análisis de Vibraciones P-101</h1>
    
    <div class="grid">
      <StatusCard 
        :valor="datosSensor.valor" 
        :estado="datosSensor.estado" 
        :unidad="datosSensor.unidad"
      />
      
      <GraficaCard 
        :nuevoValor="datosSensor.valor" 
        :color="colorActual"
      />
    </div>
  </div>

  <div class="dashboard">
    <div class="grid">
      <SenalCard 
        :valor="datos.valor" 
        :estado="datos.estado" 
        :tipoActual="tipoDeOnda"
        @cambiarTipo="handleCambioTipo" 
      />
    </div>

    <SenalGraficaCard 
      :puntos="datos.datos_onda" 
      :color="colorActual" 
    />
    <pre>{{ datos.datos_onda }}</pre>
  </div>
</template>

<style scoped>
.grid {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  padding: 20px;
}
.dashboard-layout {
  display: flex;
  gap: 30px;
  padding: 40px;
  justify-content: center;
  background: #f0f2f5;
  min-height: 100vh;
}
</style>