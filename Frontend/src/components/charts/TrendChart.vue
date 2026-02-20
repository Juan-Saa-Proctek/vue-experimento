<template>
  <div class="chart-wrapper">
    <v-chart :option="option" autoresize @click="onPointClick" />
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  data:  { type: Array,  default: () => [] },
  limit: { type: Number, default: 4.5 }
})

const emit = defineEmits(['point-click'])

function onPointClick(params) {
  if (params.componentType === 'series') {
    const point = props.data[params.dataIndex]
    if (point) {
      emit('point-click', point) 
    }
  }
}

const option = computed(() => {
  const warning  = props.limit * 0.7
  const critical = props.limit

  return {
    backgroundColor: 'transparent',
    animation: true,
    grid: { left: '8%', right: '4%', top: '10%', bottom: '12%' },
    tooltip: {
      trigger: 'axis',
      confine: true,
      backgroundColor: 'var(--color-surface3)',
      borderColor: 'var(--color-surface)',
      textStyle: { color: 'var(--color-text-dark)', fontSize: 12 },
      formatter: (params) => {
        const p      = params.find(p => p.seriesIndex === 3)
        if (!p) return ''
        const val    = Number(p.value)
        
        const estado = val >= critical
          ? `<span style="color:#b22222; font-weight:600;">● Crítico</span>`
          : val >= warning
          ? `<span style="color:#e5ff00; font-weight:600;">● Advertencia</span>`
          : `<span style="color:#008f39; font-weight:600;">● Normal</span>`

        return `${p.axisValue}<br/>RMS: <b>${val.toFixed(3)} mm/s</b><br/>${estado}`
      },
      axisPointer: {
        lineStyle: { color: 'var(--color-text-dark)', width: 1, type: 'dashed' }
      }
    },
    xAxis: {
      type: 'category',
      data: props.data.map(d => d.time),
      axisLine:  { lineStyle: { color: 'var(--color-text-dark)' } },
      axisLabel: { color: 'var(--color-text-dark)', fontSize: 10, rotate: 30 }
    },
    yAxis: {
      type: 'value',
      axisLine:  { lineStyle: { color: 'var(--color-text-dark)' } },
      axisLabel: { color: 'var(--color-text-dark)', fontSize: 10, formatter: '{value} mm/s' },
      splitLine: { lineStyle: { color: 'var(--color-text-dark)', type: 'dashed', opacity: 0.3 } },
      name: 'RMS',
      nameTextStyle: { color: 'var(--color-text-dark)' }
    },
    series: [
      // Zona verde
      {
        type: 'line', silent: true, symbol: 'none',
        lineStyle: { opacity: 0 },
        markArea: {
          silent: true,
          data: [[
            { yAxis: 0,       itemStyle: { color: 'rgba(0,143,57,0.07)' } },
            { yAxis: warning }
          ]]
        }
      },
      // Zona amarilla
      {
        type: 'line', silent: true, symbol: 'none',
        lineStyle: { opacity: 0 },
        markArea: {
          silent: true,
          data: [[
            { yAxis: warning,  itemStyle: { color: 'rgba(229,200,0,0.08)' } },
            { yAxis: critical }
          ]]
        }
      },
      // Zona roja
      {
        type: 'line', silent: true, symbol: 'none',
        lineStyle: { opacity: 0 },
        markArea: {
          silent: true,
          data: [[
            { yAxis: critical,     itemStyle: { color: 'rgba(178,34,34,0.08)' } },
            { yAxis: critical * 2 }
          ]]
        }
      },
      // Línea principal — negra con sombra
      {
        type: 'line',
        data: props.data.map(d => d.value),
        smooth: true,
        symbol: 'circle',
        symbolSize: 6,
        itemStyle: { color: '#000000' },
        lineStyle: { color: '#000000', width: 2 },
        areaStyle: {
          color: {
            type: 'linear', x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(0,0,0,0.15)' },
              { offset: 1, color: 'rgba(0,0,0,0)' }
            ]
          }
        },
        emphasis: { scale: true },
        markLine: {
          silent: true,
          symbol: ['none', 'none'],
          data: [
            {
              yAxis: warning,
              lineStyle: { color: 'var(--color-warning)', type: 'dashed', width: 1.5 },
              label: { formatter: `Advertencia ${warning.toFixed(1)} mm/s`, color: 'var(--color-warning)', fontSize: 10 }
            },
            {
              yAxis: critical,
              lineStyle: { color: 'var(--color-critical)', type: 'dashed', width: 1.5 },
              label: { formatter: `Crítico ${critical.toFixed(1)} mm/s`, color: 'var(--color-critical)', fontSize: 10 }
            }
          ]
        }
      }
    ]
  }
})
</script>

<style scoped>
.chart-wrapper {
  width: 100%;
  height: 280px;
  cursor: pointer;
}
</style>