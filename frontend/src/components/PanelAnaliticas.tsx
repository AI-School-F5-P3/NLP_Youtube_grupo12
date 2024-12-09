// src/components/PanelAnaliticas.tsx

import React from 'react';

const PanelAnaliticas: React.FC = () => {
  return (
    <div className="p-6 bg-white rounded shadow-lg text-center">
      <h2 className="text-2xl font-bold mb-4">Analíticas</h2>
      <div className="relative inline-block group">
        <button className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
          Ver Analíticas
        </button>
        {/* Tooltip */}
        <div className="absolute bottom-full mb-2 left-1/2 transform -translate-x-1/2 opacity-0 group-hover:opacity-100 transition-opacity duration-300 bg-gray-800 text-white text-sm rounded py-1 px-2">
          En proceso de implementación
        </div>
      </div>
    </div>
  );
};

export default PanelAnaliticas;
