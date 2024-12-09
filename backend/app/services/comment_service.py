# app/services/comment_service.py

from sqlalchemy.ext.asyncio import AsyncSession
from app.models.comment import Comment

async def save_comment(db: AsyncSession, video_id: int, texto: str, autor: str, prediccion_odio: float, es_toxico: bool):
    """
    Guarda un comentario analizado en la base de datos.
    """
    new_comment = Comment(
        video_id=video_id,
        texto=texto,
        autor=autor,
        prediccion_odio=prediccion_odio,
        es_toxico=es_toxico
    )
    db.add(new_comment)
    await db.commit()
    await db.refresh(new_comment)
    return new_comment
