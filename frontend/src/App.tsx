import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Layout from './components/Layout';
import MainInterface from './components/MainInterface';
import TerminosCondiciones from './pages/TerminosCondiciones';
import PoliticaPrivacidad from './pages/PoliticaPrivacidad';
import Modal from './components/Modal';
import { apiService } from './services/apiService';

function App() {
  // Eliminamos referencias a MLFlow
  const [mostrarModalBaseDatos, setMostrarModalBaseDatos] = useState(false);
  const [estadisticasBaseDatos, setEstadisticasBaseDatos] = useState(null);

  useEffect(() => {
    const obtenerDatos = async () => {
      try {
        const estadisticasDB = await apiService.obtenerEstadisticasBaseDatos();
        setEstadisticasBaseDatos(estadisticasDB);
      } catch (error) {
        console.error("Error obteniendo datos:", error);
      }
    };
    obtenerDatos();
  }, []);

  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<MainInterface />} />
          <Route path="/terminos-condiciones" element={<TerminosCondiciones />} />
          <Route path="/politica-privacidad" element={<PoliticaPrivacidad />} />
        </Routes>
        {mostrarModalBaseDatos && (
          <Modal
            title="Base de Datos"
            onClose={() => setMostrarModalBaseDatos(false)}
          >
            {estadisticasBaseDatos ? (
              <pre>{JSON.stringify(estadisticasBaseDatos, null, 2)}</pre>
            ) : (
              <p>Cargando estadísticas de la base de datos...</p>
            )}
          </Modal>
        )}
      </Layout>
    </Router>
  );
}

export default App;
