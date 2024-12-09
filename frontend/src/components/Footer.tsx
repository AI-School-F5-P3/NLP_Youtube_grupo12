import React from 'react';
import { Link } from 'react-router-dom';

const Footer: React.FC = () => {
  return (
    <footer className="bg-gray-800 text-white p-4 flex justify-between items-center">
      <div className="flex items-center">
        <img src="/images/logo.png" alt="Logo" className="h-6 w-6 mr-2" />
        <p>&copy; 2024 YouTube Detector. Todos los derechos reservados.</p>
      </div>
      <div>
        <Link to="/terminos-condiciones" className="mr-4 hover:text-gray-300">Términos y Condiciones</Link>
        <Link to="/politica-privacidad" className="hover:text-gray-300">Política de Privacidad</Link>
      </div>
    </footer>
  );
};

export default Footer;
