# app/routers/comments.py

import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas import CommentCreate, CommentOut, Analytics
from app.models.comment import Comment
from app.services.ml_service import analyze_comment, save_prediction
from app.utils.db import get_db
from sqlalchemy.sql import func

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/", response_model=CommentOut)
async def create_comment(comment: CommentCreate, db: AsyncSession = Depends(get_db)):
    """
    Crea un nuevo comentario y realiza la predicción de odio.
    """
    # Crear y guardar el comentario en la base de datos
    db_comment = Comment(texto=comment.texto, autor=comment.autor)
    db.add(db_comment)
    await db.commit()
    await db.refresh(db_comment)

    # Analizar el comentario
    analysis_result = await analyze_comment(db_comment.texto, comment.modelo)

    # Guardar predicción en la base de datos
    await save_prediction(db, db_comment.texto, analysis_result, db_comment.id)

    # Actualizar el comentario con los resultados del análisis
    db_comment.prediccion_odio = analysis_result["confianza"]
    db_comment.es_toxico = analysis_result["es_toxico"]
    await db.commit()
    await db.refresh(db_comment)

    # Devolver el comentario actualizado
    return db_comment

@router.get("/analytics", response_model=Analytics)
async def fetch_analytics(db: AsyncSession = Depends(get_db)):
    """
    Devuelve estadísticas de los comentarios analizados.
    """
    # Total de comentarios
    total_comments_query = select(func.count(Comment.id))
    total_comments = await db.scalar(total_comments_query)
    if total_comments is None:
        total_comments = 0

    # Total de comentarios de odio
    total_hate_speech_query = select(func.count(Comment.id)).where(Comment.prediccion_odio > 0.5)
    total_hate_speech = await db.scalar(total_hate_speech_query)
    if total_hate_speech is None:
        total_hate_speech = 0

    # Calcular porcentaje
    hate_percentage = (total_hate_speech / total_comments * 100) if total_comments > 0 else 0.0
    hate_percentage = round(hate_percentage, 2)

    # Categoria está hardcodeada como "general"
    categoria = "general"

    # Loggear los datos para depuración
    logger.info(f"Analytics data: total_comentarios={total_comments}, total_comentarios_odio={total_hate_speech}, porcentaje_odio={hate_percentage}, categoria={categoria}")

    return Analytics(
        total_comentarios=total_comments,
        total_comentarios_odio=total_hate_speech,
        porcentaje_odio=hate_percentage,
        categoria=categoria
    )
