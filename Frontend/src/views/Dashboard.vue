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
    datos.value = {
      valor: res.valor,
      estado: res.estado || 'Normal', 
      datos_onda: res.datos_onda || []
   }
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
  // 1. Carga inicial inmediata
  actualizar()
  fetchDatos()

  // 2. Bucle de actualización para AMBOS
  intervalo = setInterval(() => {
    actualizar()  // Actualiza GraficaCard
    fetchDatos()   // <--- ESTO hará que SenalGraficaCard reciba datos nuevos cada segundo
  }, 1000)
})

onUnmounted(() => clearInterval(intervalo))
</script>

<template>
  <div class="dashboard-wrapper">
    <header class="dashboard-header">
      <h1>Análisis de Vibraciones P-101</h1>
      <span class="status-tag" :style="{ backgroundColor: colorActual }">
        {{ datos.estado }}
      </span>
    </header>

    <main class="dashboard-grid">
      <div class="card status-zone">
        <StatusCard 
        :valor="datosSensor.valor" 
        :estado="datosSensor.estado" 
        :unidad="datosSensor.unidad" />
      </div>

      <div class="card control-zone">
        <SenalCard 
        :valor="datos.valor" 
        :estado="datos.estado" 
        :tipoActual="tipoDeOnda" 
        @cambiarTipo="handleCambioTipo" />
      </div>

      <div class="card trend-zone">
        <h3>Tendencia (RMS)</h3>
        <GraficaCard 
        :nuevoValor="datosSensor.valor" 
        :color="colorActual" />
      </div>

      <div class="card wave-zone">
        <h3>Forma de Onda en Tiempo Real</h3>
        <SenalGraficaCard 
        :puntos="datos.datos_onda" 
        :color="colorActual" />
      </div>
    </main>
  </div>
</template>

<style scoped>
.dashboard-wrapper {
  background-color: #f0f2f5;
  min-height: 100vh;
  padding: 20px;
  font-family: sans-serif;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

/* El motor del layout */
.dashboard-grid {
  display: grid;
  /* Creamos 3 columnas iguales */
  grid-template-columns: repeat(3, 1fr);
  /* Espacio entre tarjetas */
  gap: 20px;
}

.card {
  background: white;
  border-radius: 12px;
  padding: 15px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  overflow: hidden; /* Evita que las gráficas se salgan */
}

/* Hacemos que la gráfica de onda ocupe las 3 columnas de abajo */
.wave-zone {
  grid-column: span 3; 
  height: 450px; /* Le damos buena altura */
}

/* Ajustes para las gráficas pequeñas */
.trend-zone {
  height: 350px;
}

.status-tag {
  padding: 8px 16px;
  border-radius: 8px;
  color: white;
  font-weight: bold;
}

/* RESPONSIVE: Si la pantalla es pequeña, todo a una columna */
@media (max-width: 1000px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
  }
  .wave-zone {
    grid-column: span 1;
  }
}
</style>