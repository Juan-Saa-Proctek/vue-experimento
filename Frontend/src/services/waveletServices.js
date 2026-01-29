import { API_BASE_URL } from './config';

export const waveletService = {
  async getTransformada(datos) {
    const res = await fetch(`${API_BASE_URL}/analisis/wavelet`, {
      method: 'POST',
      body: JSON.stringify(datos)
    });
    return await res.json();
  }
};