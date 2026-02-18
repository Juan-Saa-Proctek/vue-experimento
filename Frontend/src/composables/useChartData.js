import { ref } from 'vue'

export function useChartData(asset) {
  const waveformData  = ref([])
  const fftData       = ref([])
  const fftFrequencies = ref([])
  const trendData     = ref([])

  function generateWaveform() {
    const rms = asset.value?.rmsActual || 1
    waveformData.value = Array.from({ length: 200 }, (_, i) =>
      +(Math.sin(i * 0.15) * rms + (Math.random() - 0.5) * 0.3).toFixed(3)
    )
  }

  function generateFFT() {
    const bins = 64
    const rms = asset.value?.rmsActual || 1
    fftFrequencies.value = Array.from({ length: bins }, (_, i) =>
      Math.round(i * (500 / bins))
    )
    fftData.value = Array.from({ length: bins }, (_, i) => {
      const base = i < 5 ? rms * 0.8 : Math.random() * rms * 0.3
      return +base.toFixed(3)
    })
  }

  function generateTrend() {
    const points = 20
    const now = Date.now()
    const rms = asset.value?.rmsActual || 1
    trendData.value = Array.from({ length: points }, (_, i) => ({
      time: new Date(now - (points - i) * 60000 * 5).toLocaleTimeString('es-CO', {
        hour: '2-digit', minute: '2-digit'
      }),
      value: +(rms + (Math.random() - 0.5) * rms * 0.4).toFixed(2)
    }))
  }

  function refreshLive() {
    generateWaveform()
    generateFFT()
  }

  function initAll() {
    generateWaveform()
    generateFFT()
    generateTrend()
  }

  return { waveformData, fftData, fftFrequencies, trendData, initAll, refreshLive }
}