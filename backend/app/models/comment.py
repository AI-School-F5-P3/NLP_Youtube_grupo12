# app/models/comment.py

from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.utils.db import Base

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey("videos.id", ondelete="CASCADE"), nullable=True)  # Relación con videos
    texto = Column(String, nullable=False)  # Texto del comentario
    autor = Column(String, default="Anónimo")  # Autor del comentario
    fecha_publicacion = Column(DateTime, default=func.now())  # Fecha de publicación
    prediccion_odio = Column(Float, nullable=True)  # Predicción de probabilidad de odio
    es_toxico = Column(Boolean, nullable=True)  # Indicador de si es tóxico o no

    # Relación con el modelo Video
    video = relationship("Video", back_populates="comentarios")
    # Relación con el modelo Predicción
    predicciones = relationship("Prediccion", back_populates="comentario", cascade="all, delete-orphan")
