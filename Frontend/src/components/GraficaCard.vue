<script setup>
import { ref, watch } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, TitleComponent } from 'echarts/components'
import VChart from 'vue-echarts'

// Registramos los módulos necesarios de ECharts
use([CanvasRenderer, LineChart, GridComponent, TooltipComponent, TitleComponent])

const props = defineProps({
  nuevoValor: Number,
  color: String
})

// Historial de datos (máximo 50 puntos para que no se sature)
const historial = ref([])
const etiquetas = ref([])

// Observamos cuando llega un nuevo valor para actualizar la gráfica
watch(() => props.nuevoValor, (val) => {
  const ahora = new Date().toLocaleTimeString()
  
  historial.value.push(val)
  etiquetas.value.push(ahora)

  // Mantener solo los últimos 50 puntos (efecto scroll)
  if (historial.value.length > 100) {
    historial.value.shift()
    etiquetas.value.shift()
  }
})

// Configuración de la gráfica
const option = ref({
  title: { text: 'Tendencia en Tiempo Real', left: 'center', textStyle: { fontSize: 14 } },
  tooltip: { trigger: 'axis' },
  xAxis: {
    type: 'category',
    data: etiquetas.value,
    boundaryGap: false
  },
  yAxis: {
    type: 'value',
    name: 'mm/s',
    min: 0,
    max: 3 // Ajustado a tu simulación
  },
  series: [{
    data: historial.value,
    type: 'line',
    smooth: true,
    showSymbol: false,
    areaStyle: { opacity: 0.2 },
    lineStyle: { color: props.color || '#42b883', width: 2 }
  }],
  animation: false // Desactivamos animación para mejor rendimiento en tiempo real
})
</script>

<template>
  <div class="card-grafica">
    <v-chart class="chart" :option="option" autoresize />
  </div>
</template>

<style scoped>
.card-grafica {
  background: white;
  border-radius: 10px;
  padding: 15px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  width: 100%;
  max-width: 800px;
  height: 350px;
}
.chart {
  height: 100%;
  width: 100%;
}
</style>