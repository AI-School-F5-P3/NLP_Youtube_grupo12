# app/models/video_model.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.utils.db import Base

class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(String, unique=True, index=True, nullable=False)  # ID único del video de YouTube
    title = Column(String, nullable=True)  # Título del video
    description = Column(String, nullable=True)  # Descripción del video

    # Relación con comentarios
    comentarios = relationship("Comment", back_populates="video", cascade="all, delete-orphan")
