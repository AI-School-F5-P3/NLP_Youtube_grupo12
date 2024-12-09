import React from 'react'
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card"

const ExplanationSection = () => {
  return (
    <Card className="mt-8 bg-white shadow-lg rounded-xl overflow-hidden">
      <CardHeader className="bg-gradient-to-r from-blue-500 to-purple-600 text-white p-6">
        <CardTitle className="text-2xl font-bold">Acerca de YouTube Detector</CardTitle>
      </CardHeader>
      <CardContent className="p-6">
        <div className="flex flex-col lg:flex-row gap-8">
          <div className="lg:w-2/3">
            <div className="bg-gray-50 shadow-inner rounded-lg p-8 py-10">
              <p className="text-lg text-gray-700 leading-relaxed mb-6">
                <strong>YouTube Detector</strong> es tu aliado estratégico en la identificación y análisis de discurso de odio en comentarios de YouTube. Gracias a una combinación de inteligencia artificial de vanguardia y modelos de aprendizaje automático, nuestra plataforma te permite descubrir, en cuestión de segundos, el verdadero tono de las interacciones en tu canal.
              </p>
              <div className="mb-6">
                <h3 className="text-xl font-semibold mb-4 text-blue-600">¿Cómo Funciona?</h3>
                <ol className="list-decimal list-inside space-y-2 text-base text-gray-700">
                  <li><strong>Introduce un comentario o la URL del video:</strong> Simplemente pega el texto o el enlace para comenzar el análisis.</li>
                  <li><strong>Nuestro IA lo procesa al instante:</strong> Con tecnología de última generación, el contenido se examina buscando patrones de odio y toxicidad.</li>
                  <li><strong>Obtén un resultado claro y preciso:</strong> Verás una indicación contundente y un grado de confianza, lo que hace más fácil tomar decisiones rápidas.</li>
                  <li><strong>Explora tendencias y patrones:</strong> Utiliza nuestras herramientas analíticas para entender a fondo las dinámicas de la conversación en tu espacio digital.</li>
                </ol>
              </div>
              <p className="text-base text-gray-700 mb-6">
                En un entorno digital donde las interacciones son cada vez más complejas, YouTube Detector actúa como tu compañero de moderación, reduciendo el estrés y el tiempo que implica filtrar manualmente comentarios ofensivos. Imagina una comunidad más sana, constructiva y respetuosa, donde tu creatividad y la de tus seguidores pueda florecer sin distracciones ni hostilidad.
              </p>
              <p className="text-base text-gray-700">
                Más que una herramienta, YouTube Detector es una inversión en la calidad de tu canal y en el fortalecimiento de relaciones positivas con tu audiencia. No aspiramos a la perfección absoluta, sino a brindarte una ayuda práctica y confiable. ¡Da el siguiente paso hacia una experiencia en línea más armoniosa y enfocada en lo que realmente importa: el intercambio de ideas valiosas!
              </p>
            </div>
          </div>
          <div className="lg:w-1/3 flex justify-center items-center">
            <div className="relative w-full h-[400px] rounded-lg overflow-hidden shadow-md">
              <img
                src="/images/datos.jpg"
                alt="Ilustración del proceso de detección de discurso de odio"
                className="w-full h-full object-cover"
                onError={(e) => {
                  e.currentTarget.src = "/placeholder.svg?height=400&width=300";
                  e.currentTarget.alt = "Imagen no disponible";
                }}
              />
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}

export default ExplanationSection
