<template>
  <div class="chart-wrapper">
    <v-chart :option="option" autoresize />
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  data:   { type: Array,  default: () => [] },
  status: { type: String, default: 'normal' }
})

const statusColor = {
  normal:   '#00c851',
  warning:  '#ffbb33',
  critical: '#ff4444',
  offline:  '#9e9e9e'
}

const option = computed(() => {
  const lineColor = statusColor[props.status] || statusColor.normal

  return {
    backgroundColor: 'transparent',
    animation: false,
    dataZoom: [
      { type: 'inside', xAxisIndex: 0, filterMode: 'none' },
      {
        type: 'slider',
        xAxisIndex: 0,
        height: 20,
        bottom: 0,
        borderColor: 'transparent',
        backgroundColor: 'rgba(0,0,0,0.05)',
        fillerColor: 'rgba(0,0,0,0.08)',
        handleStyle: { color: '#000000' }  // ← slider siempre negro
      }
    ],
    grid: { left: '8%', right: '4%', top: '10%', bottom: '20%' },
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'var(--color-surface3)',
      borderColor: 'var(--color-surface)',
      textStyle: { color: 'var(--color-text-dark)', fontSize: 12 },
      formatter: (params) => {
        const p = params[0]
        return `Muestra: ${p.dataIndex}<br/>Amplitud: <b>${p.value.toFixed(3)} mm/s</b>`
      },
      axisPointer: {
        lineStyle: { color: '#000000', width: 1, type: 'dashed' }
      }
    },
    xAxis: {
      type: 'category',
      data: props.data.map((_, i) => i),
      axisLine:  { lineStyle: { color: 'var(--color-text-dark)' } },
      axisLabel: { color: 'var(--color-text-dark)', fontSize: 10 },
      name: 'Muestras',
      nameTextStyle: { color: 'var(--color-text-dark)' }
    },
    yAxis: {
      type: 'value',
      axisLine:  { lineStyle: { color: 'var(--color-text-dark)' } },
      axisLabel: { color: 'var(--color-text-dark)', fontSize: 10, formatter: '{value} mm/s' },
      splitLine: { lineStyle: { color: 'var(--color-text-dark)', type: 'dashed', opacity: 0.3 } },
      name: 'Amplitud',
      nameTextStyle: { color: 'var(--color-text-dark)' }
    },
    series: [{
      type: 'line',
      data: props.data,
      smooth: false,
      symbol: 'none',
      lineStyle: { color: lineColor, width: 1.5 },  // ← solo aquí cambia
      areaStyle: {
        color: {
          type: 'linear', x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [
            { offset: 0, color: 'rgba(0,0,0,0.2)' },  // ← area siempre negro
            { offset: 1, color: 'rgba(0,0,0,0)' }
          ]
        }
      }
    }]
  }
})
</script>

<style scoped>
.chart-wrapper {
  width: 100%;
  height: 280px;
}
</style>