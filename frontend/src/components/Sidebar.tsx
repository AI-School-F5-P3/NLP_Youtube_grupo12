import React from 'react'
import { Link } from 'react-router-dom'
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "./ui/tooltip"
import { Youtube, Instagram, Twitter, Facebook, Shield, FileText } from 'lucide-react'

const Sidebar: React.FC = () => {
  return (
    <div className="fixed left-0 top-0 h-full w-16 bg-gray-800 flex flex-col items-center py-4 space-y-4 z-50">
      <TooltipProvider>
        <Tooltip>
          <TooltipTrigger asChild>
            <Link to="/" className="w-12 h-12 bg-red-600 rounded-full flex items-center justify-center text-white hover:bg-red-700 transition-colors duration-200">
              <Youtube size={24} />
            </Link>
          </TooltipTrigger>
          <TooltipContent>
            <p className="font-semibold">YouTube Detector</p>
          </TooltipContent>
        </Tooltip>

        <Tooltip>
          <TooltipTrigger asChild>
            <button className="w-12 h-12 bg-pink-600 rounded-full flex items-center justify-center text-white cursor-not-allowed opacity-60">
              <Instagram size={24} />
            </button>
          </TooltipTrigger>
          <TooltipContent>
            <p className="font-semibold">Instagram Detector</p>
            <p className="text-xs mt-1">(En proceso de Implementación)</p>
          </TooltipContent>
        </Tooltip>

        <Tooltip>
          <TooltipTrigger asChild>
            <button className="w-12 h-12 bg-blue-400 rounded-full flex items-center justify-center text-white cursor-not-allowed opacity-60">
              <Twitter size={24} />
            </button>
          </TooltipTrigger>
          <TooltipContent>
            <p className="font-semibold">X Detector</p>
            <p className="text-xs mt-1">(En proceso de Implementación)</p>
          </TooltipContent>
        </Tooltip>

        <Tooltip>
          <TooltipTrigger asChild>
            <button className="w-12 h-12 bg-blue-600 rounded-full flex items-center justify-center text-white cursor-not-allowed opacity-60">
              <Facebook size={24} />
            </button>
          </TooltipTrigger>
          <TooltipContent>
            <p className="font-semibold">Facebook Detector</p>
            <p className="text-xs mt-1">(En proceso de Implementación)</p>
          </TooltipContent>
        </Tooltip>

        {/* Se han quitado los enlaces a Panel de Control y Gestión de Usuarios */}

        <Tooltip>
          <TooltipTrigger asChild>
            <Link to="/politica-privacidad" target="_blank" rel="noopener noreferrer" className="w-12 h-12 bg-gray-700 rounded-full flex items-center justify-center text-white hover:bg-gray-600 transition-colors duration-200">
              <Shield size={24} />
            </Link>
          </TooltipTrigger>
          <TooltipContent>
            <p className="font-semibold">Política de Privacidad</p>
          </TooltipContent>
        </Tooltip>

        <Tooltip>
          <TooltipTrigger asChild>
            <Link to="/terminos-condiciones" target="_blank" rel="noopener noreferrer" className="w-12 h-12 bg-gray-700 rounded-full flex items-center justify-center text-white hover:bg-gray-600 transition-colors duration-200">
              <FileText size={24} />
            </Link>
          </TooltipTrigger>
          <TooltipContent>
            <p className="font-semibold">Términos y Condiciones</p>
          </TooltipContent>
        </Tooltip>
      </TooltipProvider>
    </div>
  )
}

export default Sidebar;
