# app/services/ml_service.py

from sqlalchemy.ext.asyncio import AsyncSession
from app.ml_models.transformers.inference import HateSpeechModel

# Instancia del modelo de Transformers
model_transformers = HateSpeechModel(model_path="app/ml_models/transformers")

async def analyze_comment(text: str, selected_model: str) -> dict:
    """
    Realiza el análisis del comentario usando siempre el modelo de Transformers,
    independientemente del modelo solicitado.
    """
    # Ignoramos el modelo seleccionado y usamos siempre transformers.
    probabilities = model_transformers.predict(text)
    toxic_prob = probabilities[0][1]  # Suponemos que la clase "tóxico" está en el índice 1
    return {
        "es_toxico": toxic_prob > 0.5,
        "confianza": toxic_prob
    }

async def save_prediction(db: AsyncSession, text: str, result: dict, comment_id: int):
    """
    Guarda el resultado de la predicción en la base de datos.
    """
    from app.models.prediccion import Prediccion
    prediccion = Prediccion(
        comentario_id=comment_id,
        modelo="transformers",
        es_toxico=result["es_toxico"],
        confianza=result["confianza"],
    )
    db.add(prediccion)
    await db.commit()
    await db.refresh(prediccion)
