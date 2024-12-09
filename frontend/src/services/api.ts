// src/services/api.ts

import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface ParametrosAnalizarComentario {
  text: string;
  model_name: string;
}

export interface ServicioApi {
  analizarComentario: (params: ParametrosAnalizarComentario) => Promise<any>;
  // Ahora analizarVideo enviará parámetros en la URL
  analizarVideo: (urlVideo: string, nombreModelo: string, maxComments: number) => Promise<any>;
  obtenerAnaliticas: () => Promise<any>;
}

export const servicioApi: ServicioApi = {
  analizarComentario: async (params: ParametrosAnalizarComentario) => {
    const respuesta = await api.post('/api/v1/comments/', {
      texto: params.text,
      modelo: params.model_name,
    });
    return respuesta.data;
  },

  // Ajustamos para enviar los parámetros como query params en la URL
  analizarVideo: async (urlVideo: string, nombreModelo: string, maxComments: number) => {
    // Encodeamos los valores para que puedan ser usados en la URL
    const encodedUrl = encodeURIComponent(urlVideo);
    const encodedModel = encodeURIComponent(nombreModelo);
    // Aquí pasamos los parámetros en la query, no en el body
    const respuesta = await api.post(
      `/api/v1/video/analyze?url=${encodedUrl}&model=${encodedModel}&max_comments=${maxComments}`
    );
    return respuesta.data;
  },

  obtenerAnaliticas: async () => {
    const respuesta = await api.get('/api/v1/comments/analytics');
    return respuesta.data;
  },
};

export const usarApi = (): ServicioApi => {
  return servicioApi;
};
