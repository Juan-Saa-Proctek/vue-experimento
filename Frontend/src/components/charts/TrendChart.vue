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
  limit: {
    type: Number,
    default: 4.5
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
      return `${p.axisValue}<br/>RMS: <b>${p.value} mm/s</b>`
    }
  },
  xAxis: {
    type: 'category',
    data: props.data.map(d => d.time),
    axisLine: { lineStyle: { color: '#0f3460' } },
    axisLabel: { color: '#9e9e9e', fontSize: 10, rotate: 30 }
  },
  yAxis: {
    type: 'value',
    axisLine: { lineStyle: { color: '#0f3460' } },
    axisLabel: { color: '#9e9e9e', fontSize: 10 },
    splitLine: { lineStyle: { color: '#0f3460', type: 'dashed' } },
    name: 'mm/s',
    nameTextStyle: { color: '#9e9e9e' }
  },
  series: [
    {
      name: 'RMS',
      type: 'line',
      data: props.data.map(d => d.value),
      smooth: true,
      symbol: 'circle',
      symbolSize: 4,
      lineStyle: { color: '#e94560', width: 2 },
      itemStyle: { color: '#e94560' },
      areaStyle: {
        color: {
          type: 'linear', x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [
            { offset: 0, color: 'rgba(233,69,96,0.2)' },
            { offset: 1, color: 'rgba(233,69,96,0)' }
          ]
        }
      }
    },
    {
      name: 'Límite',
      type: 'line',
      data: props.data.map(() => props.limit),
      symbol: 'none',
      lineStyle: { color: '#ffbb33', width: 1.5, type: 'dashed' },
      itemStyle: { color: '#ffbb33' }
    }
  ]
}))
</script>

<style scoped>
.chart-wrapper {
  width: 100%;
  height: 280px;
}
</style>