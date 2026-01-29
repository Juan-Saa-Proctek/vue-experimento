<script setup>
import { ref, watch } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, TitleComponent } from 'echarts/components'
import VChart from 'vue-echarts'

use([CanvasRenderer, LineChart, GridComponent, TooltipComponent, TitleComponent])

const props = defineProps({
  // Recibimos el array completo de 100 puntos desde el backend
  puntos: {
    type: Array,
    default: () => []
  },
  color: {
    type: String,
    default: '#42b883'
  }
})

// Generamos etiquetas para el eje X (del 0 al 99) para representar los puntos
const etiquetas = Array.from({ length: 100 }, (_, i) => i)

const option = ref({
  title: { 
    text: 'Forma de Onda en Tiempo Real', 
    left: 'center', 
    textStyle: { fontSize: 14 } 
  },
  tooltip: { trigger: 'axis' },
  grid: { left: '10%', right: '5%', bottom: '10%' },
  xAxis: {
    type: 'category',
    data: etiquetas,
    boundaryGap: false,
    axisLabel: { show: false } // Ocultamos números del eje X para que sea más limpio
  },
  yAxis: {
    type: 'value',
    name: 'Amplitud',
    min: -4, // Ajustado para ver los valles negativos de la señal
    max: 4   // Ajustado para ver los picos
  },
  series: [{
    data: [], // Se llenará dinámicamente
    type: 'line',
    smooth: false, // ¡Crucial! En false para que la onda cuadrada sea perfecta
    showSymbol: false,
    lineStyle: { color: props.color, width: 2 },
    areaStyle: { opacity: 0.1 }
  }],
  animation: false // Sin animación para que el refresco sea instantáneo como un osciloscopio
})

// OBSERVADOR: Cada vez que "puntos" cambie en el Dashboard, actualizamos la gráfica
watch(() => props.puntos, (nuevosPuntos) => {
  console.log("¿Llegaron puntos?", nuevosPuntos);
  if (nuevosPuntos && nuevosPuntos.length > 0) {
    option.value.series[0].data = nuevosPuntos
  }
}, { deep: true, immediate: true})

// OBSERVADOR: Por si el color cambia según el estado (Normal/Alerta)
watch(() => props.color, (nuevoColor) => {
  option.value.series[0].lineStyle.color = nuevoColor
})
</script>

<template>
  <div class="card-grafica">
    <v-chart class="chart" :option="option" autoresize />
  </div>
</template>

<style scoped>
.card-grafica {
  background: #ffffff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
  width: 100%;
  max-width: 900px;
  height: 400px;
  border: 1px solid #eaeaea;
}
.chart {
  height: 100%;
  width: 100%;
}
</style>