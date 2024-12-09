// src/components/RastreadorTiempoReal.tsx

import React, { useState, useEffect, useRef } from "react";

interface ComentarioAnalizado {
  texto: string;
  autor: string;
  es_toxico: boolean;
  prediccion_odio: number;
}

const RastreadorTiempoReal = ({ modeloSeleccionado }: { modeloSeleccionado: string }) => {
  const [urlVideo, setUrlVideo] = useState("");
  const [comentarios, setComentarios] = useState<ComentarioAnalizado[]>([]);
  const [estaSiguiendo, setEstaSiguiendo] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [wsOpen, setWsOpen] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);

  const videoIdMatch = urlVideo.match(/v=([a-zA-Z0-9_-]{11})/);
  const video_id = videoIdMatch ? videoIdMatch[1] : null;

  useEffect(() => {
    if (estaSiguiendo && video_id) {
      wsRef.current = new WebSocket("ws://localhost:8000/api/v1/live/ws");

      wsRef.current.onopen = () => {
        console.log("Conectado al WebSocket");
        setError(null);
        setWsOpen(true);
      };

      wsRef.current.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.error) {
          setError(data.error);
          return;
        }

        if (data.texto && data.autor && data.hasOwnProperty("es_toxico")) {
          setComentarios((prev) => [data, ...prev]);
        }
      };

      wsRef.current.onerror = (err) => {
        console.error("Error en WebSocket:", err);
        setError("Error en la conexión de tiempo real.");
      };

      wsRef.current.onclose = () => {
        console.log("Conexión WebSocket cerrada");
        setWsOpen(false);
      };

      return () => {
        if (wsRef.current) {
          wsRef.current.close();
        }
      };
    }
  }, [estaSiguiendo, video_id]);

  const iniciarSeguimiento = () => {
    if (!urlVideo.trim()) {
      setError("Ingrese una URL de video válida");
      return;
    }
    if (!video_id) {
      setError("La URL no contiene un ID de video de YouTube válido");
      return;
    }

    setComentarios([]);
    setEstaSiguiendo(true);
    setError(null);
  };

  const detenerSeguimiento = () => {
    setEstaSiguiendo(false);
    setWsOpen(false);
    if (wsRef.current) {
      wsRef.current.close();
    }
  };

  const enviarComentarioSimulado = () => {
    if (!wsOpen) {
      setError("La conexión no está lista, espere un momento.");
      return;
    }
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN && video_id) {
      wsRef.current.send(JSON.stringify({
        video_id: video_id,
        texto: "Mensaje de prueba en tiempo real",
        autor: "TestUser"
      }));
    }
  };

  const iniciarChatEnVivo = () => {
    if (!wsOpen) {
      setError("La conexión no está lista, espere un momento.");
      return;
    }
    if (!video_id) {
      setError("Video ID no válido.");
      return;
    }
    wsRef.current?.send(JSON.stringify({ accion: "iniciar_chat", video_id }));
  };

  const iniciarComentariosNormales = () => {
    if (!wsOpen) {
      setError("La conexión no está lista, espere un momento.");
      return;
    }
    if (!video_id) {
      setError("Video ID no válido.");
      return;
    }
    wsRef.current?.send(JSON.stringify({ accion: "iniciar_comentarios_normales", video_id }));
  };

  const tituloSeccion = "Comentarios en tiempo real";

  return (
    <div className="bg-white shadow rounded-lg p-6">
      <h2 className="text-2xl font-bold mb-4">Seguimiento de Video en Tiempo Real</h2>
      <div className="mb-4">
        <input
          type="text"
          value={urlVideo}
          onChange={(e) => setUrlVideo(e.target.value)}
          placeholder="Ingrese la URL del video"
          className="w-full p-2 border rounded mb-2"
        />
      </div>
      <button
        onClick={estaSiguiendo ? detenerSeguimiento : iniciarSeguimiento}
        disabled={urlVideo.trim() === ''}
        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:bg-gray-400"
      >
        {estaSiguiendo ? "Detener Seguimiento" : "Iniciar Seguimiento"}
      </button>

      {estaSiguiendo && (
        <div className="mt-4 space-x-2">
          <button
            onClick={iniciarChatEnVivo}
            className="bg-purple-500 text-white px-4 py-2 rounded hover:bg-purple-600"
          >
            Iniciar Chat en Vivo
          </button>
          <button
            onClick={iniciarComentariosNormales}
            className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
          >
            Iniciar Comentarios Normales
          </button>
        </div>
      )}

      {error && (
        <div className="mt-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
          {error}
        </div>
      )}

      {video_id && (
        <div className="mt-4">
          <h3 className="text-lg font-semibold mb-2">Video:</h3>
          <div className="aspect-w-16 aspect-h-9">
            <iframe
              src={`https://www.youtube.com/embed/${video_id}`}
              frameBorder="0"
              allowFullScreen
              title="YouTube Video"
              className="w-full h-96"
            ></iframe>
          </div>
        </div>
      )}

      {estaSiguiendo && comentarios.length === 0 && !error && (
        <p className="mt-4 text-gray-600">No se han detectado comentarios aún. Espera o envía uno simulado.</p>
      )}

      {estaSiguiendo && comentarios.length > 0 && (
        <div className="mt-4">
          <h3 className="text-lg font-semibold mb-2">{tituloSeccion}:</h3>
          <div className="space-y-2">
            {comentarios.map((comentario, index) => (
              <div key={index} className={`p-4 rounded ${comentario.es_toxico ? 'bg-red-100' : 'bg-green-100'}`}>
                <p className="font-bold">{comentario.autor}</p>
                <p>{comentario.texto}</p>
                <p>{comentario.es_toxico ? "Discurso de Odio Detectado" : "No se detectó Discurso de Odio"}</p>
                <p>Confianza: {(comentario.prediccion_odio * 100).toFixed(2)}%</p>
              </div>
            ))}
          </div>
          <button className="mt-4 bg-gray-300 px-3 py-2 rounded" onClick={enviarComentarioSimulado}>
            Enviar comentario simulado
          </button>
        </div>
      )}

      {!estaSiguiendo && comentarios.length === 0 && (
        <p className="mt-4">
          Ingrese la URL de un video de YouTube y presione "Iniciar Seguimiento" para establecer la conexión.<br />
          Una vez conectado, dispondrá de dos opciones:<br />
          - "Iniciar Chat en Vivo": para videos en directo.<br />
          - "Iniciar Comentarios Normales": para videos no en directo.<br />
          Si escoge la opción incorrecta, el backend le mostrará un mensaje de error, indicando que use la otra opción.
        </p>
      )}
    </div>
  );
};

export default RastreadorTiempoReal;
