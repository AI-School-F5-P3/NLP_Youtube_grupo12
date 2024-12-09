import React from 'react'
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card"
import Footer from '@/components/Footer'

const PoliticaPrivacidad = () => {
  return (
    <div className="flex flex-col min-h-screen bg-gray-100">
      <main className="flex-1 container mx-auto py-8">
        <Card className="w-full max-w-4xl mx-auto shadow-lg">
          <CardHeader className="bg-gradient-to-r from-blue-500 to-purple-600 text-white">
            <CardTitle className="text-2xl font-bold">Política de Privacidad</CardTitle>
          </CardHeader>
          <CardContent className="p-6">
            <div className="space-y-4">
              <p>
                En YouTube Hate Speech Detector, valoramos y respetamos su privacidad. Esta política describe cómo recopilamos, usamos y protegemos su información personal.
              </p>
              <h2 className="text-xl font-semibold text-blue-600">1. Información que Recopilamos</h2>
              <p>
                Recopilamos únicamente la información necesaria para proporcionar nuestro servicio de detección de discursos de odio. Esto puede incluir el contenido que usted envía para análisis y datos de uso anónimos.
              </p>
              <h2 className="text-xl font-semibold text-blue-600">2. Uso de la Información</h2>
              <p>
                Utilizamos la información recopilada exclusivamente para proporcionar y mejorar nuestro servicio. No compartimos ni vendemos su información personal a terceros.
              </p>
              <h2 className="text-xl font-semibold text-blue-600">3. Protección de Datos</h2>
              <p>
                Implementamos medidas de seguridad técnicas y organizativas para proteger su información contra acceso no autorizado, alteración, divulgación o destrucción.
              </p>
              <h2 className="text-xl font-semibold text-blue-600">4. Sus Derechos</h2>
              <p>
                Usted tiene derecho a acceder, corregir o eliminar su información personal. Si tiene alguna pregunta o solicitud relacionada con su privacidad, contáctenos a través de la información proporcionada en nuestro sitio web.
              </p>
            </div>
          </CardContent>
        </Card>
      </main>
    </div>
  )
}

export default PoliticaPrivacidad