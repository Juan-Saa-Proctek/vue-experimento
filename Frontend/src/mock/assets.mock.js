export const mockAssets = [
  {
    id: 1,
    tag: 'P-101',
    name: 'Bomba de Alimentación',
    type: 'Bomba Centrífuga',
    location: 'Área A - Piso 1',
    rpmNominal: 1750,
    status: 'normal',
    rmsActual: 1.23,
    rmsLimit: 4.5,
    lastUpdate: new Date().toISOString()
  },
  {
    id: 2,
    tag: 'M-201',
    name: 'Motor Principal',
    type: 'Motor Eléctrico',
    location: 'Área B - Piso 1',
    rpmNominal: 3600,
    status: 'warning',
    rmsActual: 3.87,
    rmsLimit: 4.5,
    lastUpdate: new Date().toISOString()
  },
  {
    id: 3,
    tag: 'C-301',
    name: 'Compresor de Aire',
    type: 'Compresor',
    location: 'Área C - Piso 2',
    rpmNominal: 2950,
    status: 'critical',
    rmsActual: 6.12,
    rmsLimit: 4.5,
    lastUpdate: new Date().toISOString()
  },
  {
    id: 4,
    tag: 'V-401',
    name: 'Ventilador Extracción',
    type: 'Ventilador',
    location: 'Área D - Techo',
    rpmNominal: 1450,
    status: 'offline',
    rmsActual: 0,
    rmsLimit: 4.5,
    lastUpdate: new Date().toISOString()
  },
  {
    id: 5,
    tag: 'P-102',
    name: 'Bomba de Recirculación',
    type: 'Bomba Centrífuga',
    location: 'Área A - Piso 2',
    rpmNominal: 1750,
    status: 'normal',
    rmsActual: 0.98,
    rmsLimit: 4.5,
    lastUpdate: new Date().toISOString()
  },
  {
    id: 6,
    tag: 'M-202',
    name: 'Motor Secundario',
    type: 'Motor Eléctrico',
    location: 'Área B - Piso 2',
    rpmNominal: 3600,
    status: 'normal',
    rmsActual: 1.45,
    rmsLimit: 4.5,
    lastUpdate: new Date().toISOString()
  }
]