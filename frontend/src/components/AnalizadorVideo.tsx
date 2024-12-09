// src/components/AnalizadorVideo.tsx

import React, { useState } from "react";
import { usarApi } from "../services/api";

interface ComentarioAnalizado {
  texto: string;
  autor: string;
  prediccion_odio: number;
  es_toxico: boolean;
}

interface VideoDetalles {
  id: number;
  video_id: string;
  title: string;
  description: string;
}

const AnalizadorVideo = ({ modeloSeleccionado }: { modeloSeleccionado: string }) => {
  const [urlVideo, setUrlVideo] = useState<string>("");
  const [comentariosAnalizados, setComentariosAnalizados] = useState<ComentarioAnalizado[]>([]);
  const [detallesVideo, setDetallesVideo] = useState<VideoDetalles | null>(null);
  const [estaCargando, setEstaCargando] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [maxComments, setMaxComments] = useState<number>(10);
  const api = usarApi();

  const analizarVideo = async () => {
    if (!urlVideo.trim()) {
      setError("Por favor ingresa una URL de YouTube.");
      return;
    }
    setEstaCargando(true);
    setError(null);
    try {
      const respuesta = await api.analizarVideo(urlVideo, modeloSeleccionado, maxComments);
      setComentariosAnalizados(respuesta.comments);
      setDetallesVideo(respuesta.video);
    } catch (err: any) {
      console.error("Error al analizar el video:", err);
      setError("Hubo un error al analizar el video. Por favor, intente de nuevo.");
    } finally {
      setEstaCargando(false);
    }
  };

  return (
    <div className="bg-white shadow rounded-lg p-6">
      <h2 className="text-2xl font-bold mb-4">Analizar Comentarios de Video</h2>
      <div className="mb-4">
        <input
          type="text"
          value={urlVideo}
          onChange={(e) => setUrlVideo(e.target.value)}
          placeholder="Ingrese URL de YouTube"
          className="w-full p-2 border rounded mb-2"
        />
        <label className="block mb-2 text-gray-700 font-semibold">Número de comentarios a analizar:</label>
        <input
          type="number"
          min={1}
          max={3000}
          value={maxComments}
          onChange={(e) => setMaxComments(parseInt(e.target.value, 10))}
          className="w-20 p-2 border rounded"
        />
      </div>
      <button
        onClick={analizarVideo}
        disabled={estaCargando || urlVideo.trim() === ''}
        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:bg-gray-400"
      >
        {estaCargando ? "Analizando..." : "Analizar"}
      </button>
      {error && (
        <div className="mt-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
          {error}
        </div>
      )}
      {detallesVideo && (
        <div className="mt-4 p-4 bg-gray-100 rounded">
          <h3 className="text-lg font-semibold mb-2">{detallesVideo.title}</h3>
          <p className="text-sm text-gray-600">{detallesVideo.description}</p>
        </div>
      )}
      {comentariosAnalizados.length > 0 && (
        <div className="mt-4">
          <h3 className="text-lg font-semibold mb-2">Resultados del análisis:</h3>
          {comentariosAnalizados.map((comentario, index) => (
            <div key={index} className={`p-4 mb-2 rounded ${comentario.es_toxico ? 'bg-red-100' : 'bg-green-100'}`}>
              <p className="font-bold">{comentario.autor}</p>
              <p>{comentario.texto}</p>
              <p>{comentario.es_toxico ? "Discurso de Odio Detectado" : "No se detectó Discurso de Odio"}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default AnalizadorVideo;
