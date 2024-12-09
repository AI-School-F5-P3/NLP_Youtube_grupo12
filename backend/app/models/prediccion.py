# app/models/prediccion.py

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.utils.db import Base

class Prediccion(Base):
    __tablename__ = "predicciones"

    id = Column(Integer, primary_key=True, index=True)
    comentario_id = Column(Integer, ForeignKey("comments.id", ondelete="CASCADE"), nullable=False)
    modelo = Column(String, nullable=False)
    es_toxico = Column(Float, nullable=False)
    confianza = Column(Float, nullable=False)

    comentario = relationship("Comment", back_populates="predicciones")
