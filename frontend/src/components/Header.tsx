import React from 'react'
import { Link } from 'react-router-dom'
import { Bell, User } from 'lucide-react'

const Header = () => {
  return (
    <header className="flex items-center justify-between p-4 bg-blue-200 text-gray-800 border-b shadow-md">
      <Link to="/" className="flex items-center space-x-2">
        <img
          src="/images/logo.png"
          alt="YouTube Hate Speech Detector Logo"
          width={40}
          height={40}
          className="w-10 h-10 object-contain"
        />
        <h1 className="text-2xl font-bold text-gray-800">YouTube Detector</h1>
      </Link>
      <nav className="flex items-center space-x-4">
        <Link to="/" className="text-gray-600 hover:text-gray-900">Inicio</Link>
        {/* Se quitaron las etiquetas de inicio de sesión */}
      </nav>
    </header>
  )
}

export default Header
