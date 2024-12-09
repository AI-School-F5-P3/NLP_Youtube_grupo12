# app/schemas.py

from pydantic import BaseModel, ConfigDict
from typing import Optional

class CommentCreate(BaseModel):
    texto: str
    autor: Optional[str] = "Anónimo"
    modelo: Optional[str] = "transformers"

class CommentOut(BaseModel):
    id: int
    texto: str
    autor: str
    prediccion_odio: Optional[float] = None
    es_toxico: Optional[bool] = None

    class Config:
        from_attributes = True

class Analytics(BaseModel):
    total_comentarios: int
    total_comentarios_odio: int
    porcentaje_odio: float
    categoria: str
