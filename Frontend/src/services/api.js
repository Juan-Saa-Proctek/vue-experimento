import axios from 'axios'

const API_BASE = `${window.location.protocol}//${window.location.hostname}:8000/api/v1`
const WS_BASE  = `${window.location.protocol === 'https:' ? 'wss' : 'ws'}://${window.location.hostname}:8000`

const http = axios.create({
  baseURL: API_BASE,
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' }
})

// Interceptor para manejar errores globalmente
http.interceptors.response.use(
  response => response.data,
  error => {
    const message = error.response?.data?.detail || 'Error de conexión con el servidor'
    return Promise.reject(new Error(message))
  }
)

export const assetsAPI = {
  getAll:    ()                    => http.get('/assets/'),
  getById:   (id)                  => http.get(`/assets/${id}`),
  create:    (data)                => http.post('/assets/', data),
  update:    (id, data)            => http.patch(`/assets/${id}`, data),
  delete:    (id)                  => http.delete(`/assets/${id}`),
}

export const alarmsAPI = {
  getAll:       (activeOnly = false) => http.get(`/alarms/?active_only=${activeOnly}`),
  getByAsset:   (assetId)            => http.get(`/alarms/asset/${assetId}`),
  create:       (data)               => http.post('/alarms/', data),
  resolve:      (alarmId)            => http.patch(`/alarms/${alarmId}/resolve`),
}

export const sensorsAPI = {
  postReading:  (data)     => http.post('/sensors/reading', data),
  getRealtime:  (assetId)  => http.get(`/sensors/realtime/${assetId}`),
}

export const historyAPI = {
  getTrend:   (assetId, hours = 24, limit = 1000) => http.get(`/history/${assetId}/trend?hours=${hours}&limit=${limit}`),
  getSummary: (assetId, hours = 24) => http.get(`/history/${assetId}/summary?hours=${hours}`),
  getFFT:     (assetId, ts)         => http.get(`/history/${assetId}/fft?timestamp=${ts}`),
}

export const settingsAPI = {
  getAssets:         ()        => http.get('/settings/assets'),
  createAsset:       (data)    => http.post('/settings/assets', data),
  deleteAsset:       (id)      => http.delete(`/settings/assets/${id}`),
  updateThreshold:   (id, rms) => http.patch(`/settings/assets/${id}/threshold`, { rms_limit: rms }),
  getProtocols:      ()        => http.get('/settings/protocols'),
  updateProtocols:   (data)    => http.post('/settings/protocols', data),
  getStatus:         ()        => http.get('/settings/status'),
  updateAsset: (id, data)      => http.patch(`/assets/${id}`, data),
}

export const pchAPI = {
  testConnection: (host, username, password) =>
    http.post('/pch/test-connection', { host, username, password }),
  syncAssets: (host, username, password) =>
    http.post('/pch/sync', { host, username, password }),
  getHosts: () => http.get('/pch/hosts'),
}

export function createAssetWebSocket(assetId, onMessage, onError) {
  const ws = new WebSocket(`${WS_BASE}/ws/${assetId}`)
  ws.onmessage = (event) => onMessage(JSON.parse(event.data))
  ws.onerror   = (error) => onError && onError(error)
  ws.onclose   = () => console.log(`WS asset ${assetId} cerrado`)
  return ws
}