export const mockAlarms = [
  {
    id: 1,
    assetId: 3,
    assetTag: 'C-301',
    assetName: 'Compresor de Aire',
    severity: 'critical',
    message: 'Vibración RMS supera el límite crítico',
    rmsValue: 6.12,
    timestamp: new Date(Date.now() - 1000 * 60 * 15).toISOString(),
    active: true
  },
  {
    id: 2,
    assetId: 2,
    assetTag: 'M-201',
    assetName: 'Motor Principal',
    severity: 'warning',
    message: 'Vibración RMS en zona de advertencia',
    rmsValue: 3.87,
    timestamp: new Date(Date.now() - 1000 * 60 * 40).toISOString(),
    active: true
  },
  {
    id: 3,
    assetId: 1,
    assetTag: 'P-101',
    assetName: 'Bomba de Alimentación',
    severity: 'warning',
    message: 'Pico transitorio detectado',
    rmsValue: 3.10,
    timestamp: new Date(Date.now() - 1000 * 60 * 120).toISOString(),
    active: false
  }
]