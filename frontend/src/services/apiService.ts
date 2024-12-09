// src/services/apiService.ts

import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const apiService = {
  // Obtener analíticas de la base de datos (comentarios)
  async obtenerEstadisticasBaseDatos(): Promise<any> {
    // Ahora las estadísticas se obtienen de /api/v1/comments/analytics
    const response = await axios.get(`${API_URL}/api/v1/comments/analytics`);
    return response.data;
  },

  // Analizar un video
  async analizarVideo(urlVideo: string, modelName: string): Promise<any> {
    const response = await axios.post(`${API_URL}/api/v1/video/analyze`, {
      url: urlVideo,
      model: modelName,
      max_comments: 10,
    });
    return response.data;
  },
};
