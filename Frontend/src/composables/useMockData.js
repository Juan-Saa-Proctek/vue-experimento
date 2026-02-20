// composables/useMockData.js
/**
 * Generadores de datos mock para desarrollo/testing
 * NO USAR EN PRODUCCIÓN
 */

export function useMockData(asset) {
  function generateWaveform() {
    const rms = asset.value?.rmsActual || 1
    return Array.from({ length: 200 }, (_, i) =>
      +(Math.sin(i * 0.15) * rms + (Math.random() - 0.5) * 0.3).toFixed(3)
    )
  }

  function generateFFT() {
    const bins = 64
    const rms = asset.value?.rmsActual || 1
    
    const frequencies = Array.from({ length: bins }, (_, i) =>
      Math.round(i * (500 / bins))
    )
    
    const fftData = Array.from({ length: bins }, (_, i) => {
      const base = i < 5 ? rms * 0.8 : Math.random() * rms * 0.3
      return +base.toFixed(3)
    })
    
    return { frequencies, fftData }
  }

  function generateTrend() {
    const points = 20
    const now = Date.now()
    const rms = asset.value?.rmsActual || 1
    
    return Array.from({ length: points }, (_, i) => {
        const pointTime = new Date(now - (points - i) * 60000 * 5)
        
        return {
        time: pointTime.toLocaleTimeString('es-CO', {
            hour: '2-digit', minute: '2-digit'
        }),
        timestamp: pointTime.toISOString(), 
        value: +(rms + (Math.random() - 0.5) * rms * 0.4).toFixed(2)
        }
    })
    }

  return {
    generateWaveform,
    generateFFT,
    generateTrend
  }
}