import React, { useState } from 'react';
import Carousel from './Carousel';
import AnalizadorMensajeIndividual from './AnalizadorMensajeIndividual';
import AnalizadorVideo from './AnalizadorVideo';
import RastreadorTiempoReal from './RastreadorTiempoReal';
import PanelAnaliticas from './PanelAnaliticas';
import ExplanationSection from './ExplanationSection';

export default function MainInterface() {
  const [pestanaActual, setPestanaActual] = useState<string>("mensaje-individual");
  const [modeloSeleccionado, setModeloSeleccionado] = useState<string>("esencial");

  const opcionesModelo = {
    esencial: "Esencial",
    conjunto: "Ensemble",
    neural: "Red Neuronal",
    transformador: "Transformers"
  };

  return (
    <div>
      <Carousel />
      <div className="bg-white shadow rounded-lg p-6 mt-4">
        <div className="mb-6">
          <div className="flex justify-between items-center mb-4">
            <div className="flex space-x-2">
              {["mensaje-individual", "analisis-video", "tiempo-real", "analiticas"].map((pestana) => (
                <button
                  key={pestana}
                  onClick={() => setPestanaActual(pestana)}
                  className={`px-4 py-2 rounded transition-colors duration-200 ${
                    pestanaActual === pestana
                      ? "bg-blue-500 text-white"
                      : "bg-gray-200 text-gray-700 hover:bg-gray-300"
                  }`}
                >
                  {pestana.split('-').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}
                </button>
              ))}
            </div>
            <div className="relative inline-block w-[250px]">
              <div className="bg-white rounded-lg shadow-md border border-gray-300 overflow-hidden transition-all duration-300 ease-in-out hover:shadow-lg hover:border-blue-500">
                <div className="bg-gray-100 px-3 py-2 border-b border-gray-300">
                  <span className="text-sm font-medium text-gray-700">Seleccionar Modelo</span>
                </div>
                <select
                  value={modeloSeleccionado}
                  onChange={(e) => setModeloSeleccionado(e.target.value)}
                  className="w-full p-2 border-none bg-white text-blue-800 focus:outline-none focus:ring-2 focus:ring-blue-500 appearance-none cursor-pointer"
                  style={{
                    backgroundImage: `url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%232c5282'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7'%3E%3C/path%3E%3C/svg%3E")`,
                    backgroundRepeat: 'no-repeat',
                    backgroundPosition: 'right 0.5rem center',
                    backgroundSize: '1.5em 1.5em',
                    paddingRight: '2.5rem',
                  }}
                >
                  {Object.entries(opcionesModelo).map(([key, value]) => (
                    <option key={key} value={key} className="bg-white text-blue-800">
                      {value}
                    </option>
                  ))}
                </select>
              </div>
            </div>
          </div>
        </div>

        <div className="mt-6">
          {pestanaActual === "mensaje-individual" && (
            <AnalizadorMensajeIndividual modeloSeleccionado={modeloSeleccionado} />
          )}
          {pestanaActual === "analisis-video" && (
            <AnalizadorVideo modeloSeleccionado={modeloSeleccionado} />
          )}
          {pestanaActual === "tiempo-real" && (
            <RastreadorTiempoReal modeloSeleccionado={modeloSeleccionado} />
          )}
          {pestanaActual === "analiticas" && <PanelAnaliticas />}
        </div>
      </div>
      <ExplanationSection />
    </div>
  );
}
