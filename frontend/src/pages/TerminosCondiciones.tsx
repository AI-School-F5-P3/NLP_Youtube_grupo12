import React from 'react'
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card"

const TerminosCondiciones = () => {
  return (
    <div className="flex flex-col min-h-screen bg-gray-100">
      <main className="flex-1 container mx-auto py-8">
        <Card className="w-full max-w-4xl mx-auto shadow-lg">
          <CardHeader className="bg-gradient-to-r from-blue-500 to-purple-600 text-white">
            <CardTitle className="text-2xl font-bold">Términos y Condiciones</CardTitle>
          </CardHeader>
          <CardContent className="p-6">
            <div className="space-y-4">
              <p>
                Bienvenido a YouTube Hate Speech Detector. Al utilizar nuestro servicio, usted acepta cumplir con los siguientes términos y condiciones:
              </p>
              <h2 className="text-xl font-semibold text-blue-600">1. Uso del Servicio</h2>
              <p>
                Nuestro servicio está diseñado para detectar discursos de odio en comentarios de YouTube. Usted se compromete a utilizar este servicio de manera ética y legal.
              </p>
              <h2 className="text-xl font-semibold text-blue-600">2. Responsabilidad del Usuario</h2>
              <p>
                Usted es responsable de cualquier contenido que analice utilizando nuestro servicio. No utilizaremos ni almacenaremos el contenido analizado más allá del tiempo necesario para proporcionar los resultados.
              </p>
              <h2 className="text-xl font-semibold text-blue-600">3. Limitaciones del Servicio</h2>
              <p>
                Aunque nos esforzamos por proporcionar resultados precisos, nuestro servicio no es infalible. Los resultados deben considerarse como una guía y no como una determinación definitiva.
              </p>
              <h2 className="text-xl font-semibold text-blue-600">4. Modificaciones</h2>
              <p>
                Nos reservamos el derecho de modificar estos términos y condiciones en cualquier momento. Los cambios entrarán en vigor inmediatamente después de su publicación en nuestro sitio web.
              </p>
            </div>
          </CardContent>
        </Card>
      </main>
    </div>
  )
}

export default TerminosCondiciones