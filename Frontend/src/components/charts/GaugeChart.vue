<template>
  <div class="chart-wrapper">
    <v-chart :option="option" autoresize />
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  value:  { type: Number, default: 0 },
  limit:  { type: Number, default: 4.5 },
  status: { type: String, default: 'normal' }
})

const option = computed(() => {
  const warning  = props.limit * 0.7
  const critical = props.limit

  return {
    backgroundColor: 'transparent',
    series: [{
      type: 'gauge',
      center: ['50%', '60%'],
      radius: '90%',
      startAngle: 200,
      endAngle:   -20,
      min: 0,
      max: props.limit * 1.2,
      splitNumber: 4,
      axisLine: {
        lineStyle: {
          width: 16,
          color: [
            [warning  / (props.limit * 1.2), '#008f39'],  // verde tu paleta
            [critical / (props.limit * 1.2), '#e5ff00'],  // amarillo tu paleta
            [1,                               '#b22222']   // rojo tu paleta
          ]
        }
      },
        pointer: {
        length: '60%',
        width: 6,
        offsetCenter: [0, '-5%'],
        itemStyle: { color: '#121212' }
        },
      axisTick: {
        distance: -20,
        splitNumber: 4,
        lineStyle: { width: 1, color: '#121212' }
      },
      splitLine: {
        distance: -24,
        length: 12,
        lineStyle: { width: 2, color: '#121212' }
      },
      axisLabel: {
        distance: -36,
        color: '#121212',
        fontSize: 10,
        formatter: (val) => val.toFixed(1)
      },
     anchor: {
      show: true,
      showAbove: false,  // ← que quede detrás de la aguja
      size: 12,
      itemStyle: {
       color: '#121212',
       borderColor: '#bfbbbb',
       borderWidth: 2
      }
     },
      title: {
        show: false,
        offsetCenter: [0, '75%'],
        fontSize: 11,
        color: '#121212'
      },
     detail: {
      valueAnimation: true,
      fontSize: 28,
      fontWeight: 700,
      offsetCenter: [0, '40%'],  // ← antes era -10%, ahora va abajo
      formatter: (val) => `${val.toFixed(2)}\nmm/s`,
      color: '#121212',
      lineHeight: 30
     },
      data: [{
        value: props.value,
        name:  'RMS Actual'
      }]
    }]
  }
})
</script>

<style scoped>
.chart-wrapper {
  width: 100%;
  height: 220px;
}
</style>