# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import comments, video, live
from app.utils.db import init_db
from app.models import comment, prediccion, video_model  # Importar todos los modelos

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await init_db()

# Rutas
app.include_router(comments.router, prefix="/api/v1/comments", tags=["Comments"])
app.include_router(video.router, prefix="/api/v1/video", tags=["Video"])
app.include_router(live.router, prefix="/api/v1/live", tags=["Live"])

@app.get("/")
async def root():
    return {"Mensaje": "Bienvenido a la API de Youtube Detector"}

import importlib
print(importlib.import_module("app.routers.video"))  # Verifica si importa el módulo correcto
