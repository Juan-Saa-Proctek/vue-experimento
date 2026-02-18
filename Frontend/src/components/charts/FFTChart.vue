<template>
  <div class="chart-wrapper">
    <v-chart :option="option" autoresize />
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  data: {
    type: Array,
    default: () => []
  },
  frequencies: {
    type: Array,
    default: () => []
  }
})

const option = computed(() => ({
  backgroundColor: 'transparent',
  grid: { left: '8%', right: '4%', top: '15%', bottom: '12%' },
  tooltip: {
    trigger: 'axis',
    backgroundColor: '#1a1a2e',
    borderColor: '#0f3460',
    textStyle: { color: '#e0e0e0' },
    formatter: (params) => {
      const p = params[0]
      return `${p.axisValue} Hz<br/>Amplitud: <b>${p.value.toFixed(3)}</b>`
    }
  },
  xAxis: {
    type: 'category',
    data: props.frequencies,
    axisLine: { lineStyle: { color: '#0f3460' } },
    axisLabel: { color: '#9e9e9e', fontSize: 10 },
    name: 'Frecuencia (Hz)',
    nameTextStyle: { color: '#9e9e9e' }
  },
  yAxis: {
    type: 'value',
    axisLine: { lineStyle: { color: '#0f3460' } },
    axisLabel: { color: '#9e9e9e', fontSize: 10 },
    splitLine: { lineStyle: { color: '#0f3460', type: 'dashed' } },
    name: 'Amplitud',
    nameTextStyle: { color: '#9e9e9e' }
  },
  series: [{
    type: 'bar',
    data: props.data,
    itemStyle: {
      color: {
        type: 'linear', x: 0, y: 0, x2: 0, y2: 1,
        colorStops: [
          { offset: 0, color: '#e94560' },
          { offset: 1, color: 'rgba(233,69,96,0.3)' }
        ]
      }
    },
    barMaxWidth: 6
  }]
}))
</script>

<style scoped>
.chart-wrapper {
  width: 100%;
  height: 280px;
}
</style>