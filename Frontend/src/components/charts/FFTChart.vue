<template>
  <div class="chart-wrapper">
    <v-chart :option="option" autoresize />
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  data:        { type: Array,  default: () => [] },
  frequencies: { type: Array,  default: () => [] },
  rpmNominal:  { type: Number, default: 1750 }
})

const option = computed(() => {
  const freq1x = props.rpmNominal / 60
  const freq2x = freq1x * 2
  const freq3x = freq1x * 3

  return {
    backgroundColor: 'transparent',
    animation: false,
    dataZoom: [
      { type: 'inside', xAxisIndex: 0 },
      {
        type: 'slider',
        xAxisIndex: 0,
        height: 20,
        bottom: 0,
        borderColor: 'transparent',
        backgroundColor: 'rgba(0,0,0,0.05)',
        fillerColor: 'rgba(0,0,0,0.08)',
        handleStyle: { color: '#000000' }
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
        const freq     = props.frequencies[p.dataIndex] || 0
        const harmonic = freq > 0 ? (freq / freq1x).toFixed(1) : '—'
        return `Frecuencia: <b>${freq} Hz</b><br/>Amplitud: <b>${p.value.toFixed(4)}</b><br/>Armónico: <b>${harmonic}x RPM</b>`
      },
      axisPointer: {
        lineStyle: { color: '#000000', width: 1, type: 'dashed' }
      }
    },
    xAxis: {
      type: 'category',
      data: props.frequencies.map(f => `${f}Hz`),
      axisLine:  { lineStyle: { color: 'var(--color-text-dark)' } },
      axisLabel: { color: 'var(--color-text-dark)', fontSize: 9, rotate: 30 },
      name: 'Frecuencia (Hz)',
      nameTextStyle: { color: 'var(--color-text-dark)' }
    },
    yAxis: {
      type: 'value',
      axisLine:  { lineStyle: { color: 'var(--color-text-dark)' } },
      axisLabel: { color: 'var(--color-text-dark)', fontSize: 10 },
      splitLine: { lineStyle: { color: 'var(--color-text-dark)', type: 'dashed', opacity: 0.3 } },
      name: 'Amplitud',
      nameTextStyle: { color: 'var(--color-text-dark)' }
    },
    series: [{
      type: 'bar',
      data: props.data,
      barMaxWidth: 6,
      itemStyle: {
        color: {
          type: 'linear', x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [
            { offset: 0, color: 'rgba(0,0,0,0.8)' },
            { offset: 1, color: 'rgba(0,0,0,0.2)' }
          ]
        }
      },
      markLine: {
        silent: false,
        symbol: ['none', 'none'],
        label: { fontSize: 10, color: 'var(--color-text-dark)' },
        lineStyle: { type: 'dashed', width: 1.5 },
        data: [
          {
            name: '1x',
            xAxis: props.frequencies.findIndex(f => Math.abs(f - freq1x) < 5),
            lineStyle: { color: '#ffbb33' },
            label: { formatter: '1x', color: '#ffbb33' }
          },
          {
            name: '2x',
            xAxis: props.frequencies.findIndex(f => Math.abs(f - freq2x) < 5),
            lineStyle: { color: '#ff8800' },
            label: { formatter: '2x', color: '#ff8800' }
          },
          {
            name: '3x',
            xAxis: props.frequencies.findIndex(f => Math.abs(f - freq3x) < 5),
            lineStyle: { color: '#ff4444' },
            label: { formatter: '3x', color: '#ff4444' }
          },
        ].filter(m => m.xAxis >= 0)
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