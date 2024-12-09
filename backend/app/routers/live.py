# app/routers/live.py

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.video_service import get_or_create_video
from app.services.comment_service import save_comment
from app.services.ml_service import analyze_comment
from app.services.websocket_service import WebSocketManager
from app.utils.db import get_db
import asyncio
from app.services.youtube_service import start_live_chat_loop, start_regular_comments_polling, is_live_streaming

router = APIRouter()
manager = WebSocketManager()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, db: AsyncSession = Depends(get_db)):
    """
    WebSocket para procesar comentarios en tiempo real y chat en vivo.
    Casos:
    - Comentario manual: { "video_id":"...", "texto":"...", "autor":"..." }
    - Iniciar chat en vivo: { "accion":"iniciar_chat", "video_id":"..." }
    - Iniciar comentarios normales: { "accion":"iniciar_comentarios_normales", "video_id":"..." }
    """
    await manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_json()

            # Comentario manual
            if "video_id" in data and "texto" in data and "autor" in data and "accion" not in data:
                video_id = data["video_id"]
                comment_text = data["texto"]
                author = data["autor"]

                analysis_result = await analyze_comment(comment_text, "transformers")
                video = await get_or_create_video(db, video_id=video_id)
                saved_comment = await save_comment(
                    db,
                    video_id=video.id,
                    texto=comment_text,
                    autor=author,
                    prediccion_odio=analysis_result["confianza"],
                    es_toxico=analysis_result["es_toxico"]
                )

                await websocket.send_json(
                    {
                        "texto": saved_comment.texto,
                        "autor": saved_comment.autor,
                        "es_toxico": saved_comment.es_toxico,
                        "prediccion_odio": saved_comment.prediccion_odio
                    }
                )

            # Iniciar chat en vivo
            elif "accion" in data and data["accion"] == "iniciar_chat" and "video_id" in data:
                video_id = data["video_id"]
                # Si el video está en vivo, iniciamos el loop
                if is_live_streaming(video_id):
                    asyncio.create_task(start_live_chat_loop(video_id, db, manager, model_name="transformers"))
                else:
                    # Si no está en vivo, podrías enviar un mensaje de error al frontend
                    await websocket.send_json({"error":"El video no tiene chat en vivo."})

            # Iniciar comentarios normales en tiempo real
            elif "accion" in data and data["accion"] == "iniciar_comentarios_normales" and "video_id" in data:
                video_id = data["video_id"]
                if not is_live_streaming(video_id):
                    # Iniciar el polling de comentarios normales
                    asyncio.create_task(start_regular_comments_polling(video_id, db, manager, model_name="transformers", max_results=5))
                else:
                    # Si el video es en vivo, ya está el otro modo
                    await websocket.send_json({"error":"El video es en vivo, use iniciar_chat."})

            else:
                # Mensaje no reconocido
                await websocket.send_json({"error":"Mensaje no reconocido."})

    except WebSocketDisconnect:
        manager.disconnect(websocket)
