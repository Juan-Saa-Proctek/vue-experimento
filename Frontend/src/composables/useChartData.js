import { ref } from 'vue'
import { createAssetWebSocket } from '../services/api.js'

export function useChartData(asset) {
  const waveformData   = ref([])
  const fftData        = ref([])
  const fftFrequencies = ref([])
  const trendData      = ref([])

  let ws = null

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

  // Conecta WebSocket y actualiza gráficas con data real
  function connectWebSocket(assetId) {
    if (ws) ws.close()

    ws = createAssetWebSocket(
      assetId,
      (data) => {
        // data viene del backend: { rms, waveform, fft_data, frequencies, timestamp }
        if (data.waveform)    waveformData.value   = data.waveform
        if (data.fft_data)    fftData.value         = data.fft_data
        if (data.frequencies) fftFrequencies.value  = data.frequencies

        // Agregar punto a la tendencia
        trendData.value.push({
          time:  new Date(data.timestamp).toLocaleTimeString('es-CO', {
            hour: '2-digit', minute: '2-digit'
          }),
          value: data.rms
        })

        // Mantener solo los últimos 30 puntos
        if (trendData.value.length > 30) trendData.value.shift()
      },
      (error) => console.error('WS error:', error)
    )
  }

  function disconnectWebSocket() {
    if (ws) {
      ws.close()
      ws = null
    }
  }

  function refreshLive() {
    // Si no hay WS activo, genera data simulada como fallback
    if (!ws || ws.readyState !== WebSocket.OPEN) {
      generateWaveform()
      generateFFT()
    }
  }

  function initAll(assetId = null) {
    generateWaveform()
    generateFFT()
    generateTrend()
    if (assetId) connectWebSocket(assetId)
  }

  return {
    waveformData, fftData, fftFrequencies, trendData,
    initAll, refreshLive, connectWebSocket, disconnectWebSocket
  }
}