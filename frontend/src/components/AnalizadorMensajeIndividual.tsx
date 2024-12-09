import React, { useState } from "react";
import { usarApi, ParametrosAnalizarComentario } from "../services/api";

const AnalizadorMensajeIndividual = ({ modeloSeleccionado }: { modeloSeleccionado: string }) => {
  const [texto, setTexto] = useState("");
  const [resultado, setResultado] = useState<any>(null);
  const [estaCargando, setEstaCargando] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const api = usarApi();

  const manejarAnalisis = async () => {
    setEstaCargando(true);
    setError(null);
    try {
      const params: ParametrosAnalizarComentario = {
        text: texto,
        model_name: modeloSeleccionado
      };
      const respuesta = await api.analizarComentario(params);
      setResultado(respuesta);
    } catch (error) {
      console.error("Error al analizar el comentario:", error);
      setError("Hubo un error al analizar el comentario. Por favor, intente de nuevo.");
    } finally {
      setEstaCargando(false);
    }
  };

  return (
    <div className="bg-gradient-to-br from-blue-50 to-indigo-100 shadow-lg rounded-lg p-8 transition-all duration-300 hover:shadow-xl">
      <div className="mb-6">
        <h2 className="text-3xl font-bold mb-2 text-indigo-800">Analizador de Comentario Individual</h2>
        <p className="text-indigo-600">Ingrese el texto que desea analizar</p>
      </div>
      <div className="mb-6">
        <label htmlFor="texto-analizar" className="block text-sm font-medium text-indigo-700 mb-2">
          Texto a analizar
        </label>
        <textarea
          id="texto-analizar"
          value={texto}
          onChange={(e) => setTexto(e.target.value)}
          placeholder="Ingrese el texto a analizar"
          className="w-full p-3 border border-indigo-300 rounded-md min-h-[120px] focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all duration-300"
        />
      </div>
      <div className="flex flex-col space-y-6">
        <button
          onClick={manejarAnalisis}
          disabled={estaCargando || texto.trim() === ''}
          className={`px-6 py-3 rounded-md text-white font-semibold transition-all duration-300 ${
            estaCargando || texto.trim() === ''
              ? 'bg-gray-400 cursor-not-allowed'
              : 'bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-opacity-50'
          }`}
        >
          {estaCargando ? "Analizando..." : "Analizar"}
        </button>
        {error && (
          <div className="bg-red-50 border-l-4 border-red-500 text-red-700 p-4 rounded-md shadow-md transition-all duration-300" role="alert">
            <p className="font-bold">Error</p>
            <p>{error}</p>
          </div>
        )}
        {resultado && (
          <div 
            className={`p-4 rounded-md shadow-md transition-all duration-300 ${
              resultado.es_toxico 
                ? 'bg-red-50 border-l-4 border-red-500 text-red-700' 
                : 'bg-green-50 border-l-4 border-green-500 text-green-700'
            }`} 
            role="alert"
            aria-live="polite"
          >
            <p className="font-bold">
              {resultado.es_toxico ? "Comentario de odio detectado" : "No se detectó comentario de odio"}
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default AnalizadorMensajeIndividual;