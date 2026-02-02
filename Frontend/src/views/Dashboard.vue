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
        Estado: {{ datos.estado }}
      </span>
    </header>

    <main class="dashboard-layout">
      <section class="main-content">
        <div class="card-container">
          <SenalCard 
            :valor="datos.valor" 
            :estado="datos.estado" 
            :tipoActual="tipoDeOnda"
            @cambiarTipo="handleCambioTipo" 
          />
        </div>

        <div class="card-container">
          <h3>Forma de Onda (Tiempo Real)</h3>
          <SenalGraficaCard 
            :puntos="datos.datos_onda" 
            :color="colorActual" 
          />
        </div>
      </section>

      <aside class="sidebar-charts">
        <StatusCard 
          :valor="datosSensor.valor" 
          :estado="datosSensor.estado" 
          :unidad="datosSensor.unidad"
        />
        
        <div class="trend-container">
          <h3>Tendencia de Vibración</h3>
          <GraficaCard 
            :nuevoValor="datosSensor.valor" 
            :color="colorActual"
          />
        </div>
      </aside>
    </main>
  </div>
</template>

<style scoped>
.dashboard-wrapper {
  background-color: #f4f7f9;
  min-height: 100vh;
  padding: 20px 40px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  border-bottom: 2px solid #ddd;
  padding-bottom: 10px;
}

.dashboard-layout {
  display: flex;
  gap: 25px;
  align-items: flex-start;
}

/* Columna principal (70% aprox) */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* Columna lateral (30% aprox) */
.sidebar-charts {
  width: 380px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  position: sticky; /* Se queda fija al hacer scroll */
  top: 20px;
}

.card-container, .trend-container {
  background: white;
  border-radius: 12px;
  padding: 15px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}

h3 {
  margin-top: 0;
  color: #34495e;
  font-size: 1.1rem;
  margin-bottom: 15px;
}

.status-tag {
  padding: 6px 15px;
  border-radius: 20px;
  color: white;
  font-weight: bold;
  text-transform: uppercase;
  font-size: 0.8rem;
}

/* Responsive para pantallas pequeñas */
@media (max-width: 1100px) {
  .dashboard-layout {
    flex-direction: column;
  }
  .sidebar-charts {
    width: 100%;
    position: static;
  }
}
</style>