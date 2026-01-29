import { API_BASE_URL } from './config';

export const sensorService = {
  async getVibracion() {
    try {
      const respuesta = await fetch(`${API_BASE_URL}/sensor`);
      if (!respuesta.ok) throw new Error('Error en la red');
      return await respuesta.json();
    } catch (error) {
      console.error("Error en sensorService:", error);
      throw error;
    }
  }
};

export const senalService = {
 async getSenal(tipo) {
    try {
      const respuesta = await fetch(`${API_BASE_URL}/senal/${tipo}`);;
      if (!respuesta.ok) throw new Error('Error en la red');
      return await respuesta.json();
    } catch (error) {
      console.error("Error en sensorService:", error);
      throw error;
    }
  }
};