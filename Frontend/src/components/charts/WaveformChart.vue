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
  }
})

const option = computed(() => ({
  backgroundColor: 'transparent',
  grid: { left: '8%', right: '4%', top: '15%', bottom: '12%' },
  tooltip: {
    trigger: 'axis',
    backgroundColor: '#1a1a2e',
    borderColor: '#0f3460',
    textStyle: { color: '#e0e0e0' }
  },
  xAxis: {
    type: 'category',
    data: props.data.map((_, i) => i),
    axisLine: { lineStyle: { color: '#0f3460' } },
    axisLabel: { color: '#9e9e9e', fontSize: 10 },
    name: 'Muestras',
    nameTextStyle: { color: '#9e9e9e' }
  },
  yAxis: {
    type: 'value',
    axisLine: { lineStyle: { color: '#0f3460' } },
    axisLabel: { color: '#9e9e9e', fontSize: 10 },
    splitLine: { lineStyle: { color: '#0f3460', type: 'dashed' } },
    name: 'mm/s',
    nameTextStyle: { color: '#9e9e9e' }
  },
  series: [{
    type: 'line',
    data: props.data,
    smooth: false,
    symbol: 'none',
    lineStyle: { color: '#00c851', width: 1.5 },
    areaStyle: {
      color: {
        type: 'linear', x: 0, y: 0, x2: 0, y2: 1,
        colorStops: [
          { offset: 0, color: 'rgba(0,200,81,0.2)' },
          { offset: 1, color: 'rgba(0,200,81,0)' }
        ]
      }
    }
  }]
}))
</script>

<style scoped>
.chart-wrapper {
  width: 100%;
  height: 280px;
}

.chart-wrapper .echarts {
  width: 100%;
  height: 100%;
}
</style>