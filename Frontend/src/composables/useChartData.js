import { ref } from 'vue'
import { createAssetWebSocket, historyAPI } from '../services/api.js'
import { useMockData } from './useMockData.js'

/**
 * Composable para manejo de datos de gráficas en tiempo real
 * Usa WebSocket para datos live, mock data como fallback
 */
export function useChartData(asset) {
  const waveformData   = ref([])
  const fftData        = ref([])
  const fftFrequencies = ref([])
  const trendData      = ref([])

  let ws = null

  // 🔧 SEPARADO: Mock data solo cuando sea necesario
  const mockData = useMockData(asset)

  // WebSocket connection
  function connectWebSocket(assetId) {
    if (ws) ws.close()

    ws = createAssetWebSocket(
      assetId,
      (data) => {
        // Actualizar con datos reales del WebSocket
        if (data.waveform)    waveformData.value  = data.waveform
        if (data.fft_data)    fftData.value       = data.fft_data
        if (data.frequencies) fftFrequencies.value = data.frequencies

        // 🔧 FIX: Guardar AMBOS formatos de timestamp
        trendData.value.push({
          time: new Date(data.timestamp).toLocaleTimeString('es-CO', {
            hour: '2-digit', minute: '2-digit'
          }),
          timestamp: data.timestamp,  // 🔧 NUEVO: ISO completo para backend
          value: data.rms
        })

        // Mantener últimos 30 puntos
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

  // Refresh manual (usa mock solo si WS no está conectado)
  function refreshLive() {
    if (!ws || ws.readyState !== WebSocket.OPEN) {
      console.warn(' WebSocket no conectado, usando datos mock')
      waveformData.value = mockData.generateWaveform()
      const { frequencies, fftData: mockFFT } = mockData.generateFFT()
      fftFrequencies.value = frequencies
      fftData.value = mockFFT
    }
  }

  async function loadHistoricalTrend(assetId, hours = 24) {
    try {
      const response = await historyAPI.getTrend(assetId, hours)
      
      
      const data = Array.isArray(response) ? response : response.data || []
      
      trendData.value = data.map(point => ({
        time: new Date(point.timestamp).toLocaleTimeString('es-CO', {
          hour: '2-digit', minute: '2-digit'
        }),
        timestamp: point.timestamp,  
        value: point.rms
      }))
      
      console.log(`✅ Cargados ${trendData.value.length} puntos de tendencia`)
    } catch (e) {
      console.warn('⚠️ No se pudo cargar tendencia histórica:', e.message)
    
      trendData.value = mockData.generateTrend()
    }
  }

  // Inicialización
  async function initAll(assetId = null) {
    // Inicializar con mock mientras carga
    waveformData.value = mockData.generateWaveform()
    const { frequencies, fftData: mockFFT } = mockData.generateFFT()
    fftFrequencies.value = frequencies
    fftData.value = mockFFT

    if (assetId) {
      // 🔧 NUEVO: Cargar tendencia histórica primero
      await loadHistoricalTrend(assetId, 24)
      
      // Luego conectar WebSocket para datos en vivo
      connectWebSocket(assetId)
    } else {
      // Sin assetId, usar mock
      trendData.value = mockData.generateTrend()
    }
  }

  // FFT histórica (datos reales del backend)
  async function fetchHistoricalFFT(assetId, timestamp) {
    try {
      const response = await historyAPI.getFFT(assetId, timestamp)
      return {
        fftData:     response.fft_data,
        frequencies: response.frequencies,
        rms:         response.rms,
        timestamp:   response.timestamp,
      }
    } catch (e) {
      console.warn('FFT histórica no disponible:', e.message)
      // Fallback: retorna la FFT actual
      return {
        fftData:     fftData.value,
        frequencies: fftFrequencies.value,
        rms:         null,
        timestamp:   timestamp,
      }
    }
  }

  return {
    // Estado
    waveformData, 
    fftData, 
    fftFrequencies, 
    trendData,
    
    // Métodos
    initAll, 
    refreshLive, 
    connectWebSocket, 
    disconnectWebSocket,
    fetchHistoricalFFT,
    loadHistoricalTrend, 
  }
}