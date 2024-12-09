# app/services/youtube_service.py

# app/services/youtube_service.py

import os
import re
import requests
import asyncio
import logging
from typing import List, Dict, Optional
from app.services.ml_service import analyze_comment
from app.services.comment_service import save_comment
from app.services.video_service import get_or_create_video
from app.services.websocket_service import WebSocketManager
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
if not YOUTUBE_API_KEY:
    raise RuntimeError("YOUTUBE_API_KEY no está configurada en el archivo .env")

logger = logging.getLogger(__name__)

def extract_video_id(url: str) -> str:
    match = re.search(r"v=([a-zA-Z0-9_-]{11})", url)
    if not match:
        raise ValueError("URL de video no válida.")
    return match.group(1)

def fetch_video_details(video_url: str) -> dict:
    """
    Obtiene los detalles básicos de un video de YouTube.
    """
    video_id = extract_video_id(video_url)
    req_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={YOUTUBE_API_KEY}"
    response = requests.get(req_url)
    if response.status_code != 200:
        raise RuntimeError("Error al obtener detalles del video de YouTube.")

    data = response.json()
    if "items" not in data or len(data["items"]) == 0:
        raise ValueError("No se encontró información para este video.")

    snippet = data["items"][0]["snippet"]
    return {
        "video_id": video_id,
        "title": snippet.get("title", "Sin título"),
        "description": snippet.get("description", "Sin descripción"),
        "embed_url": f"https://www.youtube.com/embed/{video_id}"
    }

async def fetch_comments_from_video(video_id: str, model: str, max_comments: int = 10) -> List[Dict]:
    """
    Obtiene comentarios de un video de YouTube y los analiza.
    """
    req_url = f"https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={video_id}&key={YOUTUBE_API_KEY}&maxResults={max_comments}"
    response = requests.get(req_url)

    if response.status_code != 200:
        raise RuntimeError("Error al obtener comentarios del video de YouTube.")

    data = response.json()
    if "items" not in data:
        raise ValueError("No se encontraron comentarios para este video.")

    comments = []
    for item in data["items"]:
        snippet = item["snippet"]["topLevelComment"]["snippet"]
        comments.append({
            "texto": snippet["textOriginal"],
            "autor": snippet["authorDisplayName"]
        })

    analyzed_comments = []
    for comment in comments:
        analysis = await analyze_comment(comment["texto"], model)
        analyzed_comments.append({
            "texto": comment["texto"],
            "autor": comment["autor"],
            "es_toxico": analysis["es_toxico"],
            "confianza": analysis["confianza"]
        })

    return analyzed_comments

async def analyze_comment_list(comments: List[Dict], db: AsyncSession, video_id: str, manager: WebSocketManager, model_name: str = "transformers"):
    """
    Analiza una lista de comentarios (texto, autor) con el modelo,
    los guarda y los envía por WebSocket.
    """
    video = await get_or_create_video(db, video_id=video_id)

    for comment in comments:
        texto = comment["texto"]
        autor = comment["autor"]
        analysis_result = await analyze_comment(texto, model_name)
        saved_comment = await save_comment(
            db,
            video_id=video.id,
            texto=texto,
            autor=autor,
            prediccion_odio=analysis_result["confianza"],
            es_toxico=analysis_result["es_toxico"]
        )

        msg = {
            "texto": saved_comment.texto,
            "autor": saved_comment.autor,
            "es_toxico": saved_comment.es_toxico,
            "prediccion_odio": saved_comment.prediccion_odio
        }
        await manager.broadcast(msg)

def is_live_streaming(video_id: str) -> bool:
    """
    Verifica si el video está en vivo comprobando liveStreamingDetails.
    """
    url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "id": video_id,
        "part": "snippet,liveStreamingDetails",
        "key": YOUTUBE_API_KEY
    }
    resp = requests.get(url, params=params)
    if resp.status_code != 200:
        return False

    data = resp.json()
    if "items" not in data or len(data["items"]) == 0:
        return False

    live_details = data["items"][0].get("liveStreamingDetails", {})
    return "activeLiveChatId" in live_details

async def get_active_live_chat_id(video_id: str) -> Optional[str]:
    url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "id": video_id,
        "part": "snippet,liveStreamingDetails",
        "key": YOUTUBE_API_KEY
    }
    resp = requests.get(url, params=params)
    if resp.status_code != 200:
        raise RuntimeError("Error al obtener detalles del video (liveStreamingDetails).")

    data = resp.json()
    if "items" not in data or len(data["items"]) == 0:
        return None

    live_details = data["items"][0].get("liveStreamingDetails", {})
    return live_details.get("activeLiveChatId")

async def fetch_live_chat_messages(liveChatId: str, pageToken: Optional[str] = None) -> dict:
    url = "https://www.googleapis.com/youtube/v3/liveChat/messages"
    params = {
        "liveChatId": liveChatId,
        "part": "snippet,authorDetails",
        "key": YOUTUBE_API_KEY
    }
    if pageToken:
        params["pageToken"] = pageToken

    resp = requests.get(url, params=params)
    if resp.status_code != 200:
        raise RuntimeError(f"Error al obtener mensajes del chat en vivo: {resp.text}")

    return resp.json()

async def start_live_chat_loop(video_id: str, db: AsyncSession, manager: WebSocketManager, model_name: str = "transformers"):
    activeLiveChatId = await get_active_live_chat_id(video_id)
    if not activeLiveChatId:
        logger.info("El video no es en directo o no tiene chat en vivo.")
        return

    nextPageToken = None

    while True:
        try:
            data = await fetch_live_chat_messages(activeLiveChatId, nextPageToken)
        except Exception as e:
            logger.error(f"Error obteniendo chat en vivo: {e}")
            break

        items = data.get("items", [])
        pollingInterval = data.get("pollingIntervalMillis", 5000)
        nextPageToken = data.get("nextPageToken")

        comments = []
        for item in items:
            snippet = item.get("snippet", {})
            author = item.get("authorDetails", {})
            type_event = snippet.get("type")
            display_message = snippet.get("displayMessage")

            # Solo procesar mensajes de texto normal
            if type_event == "textMessageEvent" and display_message:
                texto = display_message
                autor = author.get("displayName", "Anónimo")
                comments.append({"texto": texto, "autor": autor})
            else:
                # Ignorar mensajes que no sean de tipo texto
                continue

        if comments:
            await analyze_comment_list(comments, db, video_id, manager, model_name)

        await asyncio.sleep(pollingInterval / 1000.0)

async def fetch_top_comments(video_id: str, max_results: int = 5) -> List[Dict]:
    """
    Obtiene los últimos comentarios del video no en directo (ordenados por tiempo).
    """
    url = "https://www.googleapis.com/youtube/v3/commentThreads"
    params = {
        "part": "snippet",
        "videoId": video_id,
        "key": YOUTUBE_API_KEY,
        "maxResults": max_results,
        "order": "time"
    }
    resp = requests.get(url, params=params)
    if resp.status_code != 200:
        raise RuntimeError("Error al obtener comentarios del video (no en vivo).")

    data = resp.json()
    if "items" not in data:
        return []

    comments = []
    for item in data["items"]:
        snippet = item["snippet"]["topLevelComment"]["snippet"]
        comments.append({
            "texto": snippet["textOriginal"],
            "autor": snippet["authorDisplayName"],
            "publishedAt": snippet["publishedAt"]
        })
    return comments

async def start_regular_comments_polling(video_id: str, db: AsyncSession, manager: WebSocketManager, model_name: str = "transformers", max_results: int = 5):
    """
    Realiza polling de comentarios normales en un video no en vivo.
    """
    old_comments = await fetch_top_comments(video_id, max_results=max_results)
    old_comments_sorted = sorted(old_comments, key=lambda c: c["publishedAt"])

    last_published = old_comments_sorted[-1]["publishedAt"] if old_comments_sorted else None

    initial_comments = [{"texto": c["texto"], "autor": c["autor"]} for c in old_comments_sorted]
    await analyze_comment_list(initial_comments, db, video_id, manager, model_name)

    # Polling cada 10s
    while True:
        await asyncio.sleep(10)
        try:
            new_batch = await fetch_top_comments(video_id, max_results=max_results)
        except Exception as e:
            logger.error(f"Error obteniendo comentarios regulares: {e}")
            continue

        new_batch_sorted = sorted(new_batch, key=lambda c: c["publishedAt"])

        new_comments = []
        if last_published:
            for c in new_batch_sorted:
                if c["publishedAt"] > last_published:
                    new_comments.append({"texto": c["texto"], "autor": c["autor"]})
        else:
            new_comments = [{"texto": c["texto"], "autor": c["autor"]} for c in new_batch_sorted]

        if new_comments:
            await analyze_comment_list(new_comments, db, video_id, manager, model_name)
            newest = new_batch_sorted[-1]["publishedAt"]
            last_published = newest
