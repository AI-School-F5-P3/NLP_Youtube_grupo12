# app/routers/video.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.video_service import get_or_create_video
from app.services.comment_service import save_comment
from app.services.youtube_service import fetch_video_details, fetch_comments_from_video
from app.utils.db import get_db

router = APIRouter()

@router.post("/analyze")
async def analyze_video(
    url: str,
    model: str = "transformers",
    max_comments: int = Query(10, ge=1, le=3000),
    db: AsyncSession = Depends(get_db)
):
    try:
        video_details = fetch_video_details(url)
        video = await get_or_create_video(
            db,
            video_id=video_details["video_id"],
            title=video_details["title"],         # Aseguramos pasar title
            description=video_details["description"]  # Aseguramos pasar description
        )

        comments = await fetch_comments_from_video(
            video_details["video_id"], model=model, max_comments=max_comments
        )

        analyzed_comments = []
        for comment in comments:
            saved_comment = await save_comment(
                db,
                video_id=video.id,
                texto=comment["texto"],
                autor=comment["autor"],
                prediccion_odio=comment["confianza"],
                es_toxico=comment["es_toxico"]
            )
            analyzed_comments.append({
                "texto": saved_comment.texto,
                "autor": saved_comment.autor,
                "prediccion_odio": saved_comment.prediccion_odio,
                "es_toxico": saved_comment.es_toxico
            })

        return {
            "video": {
                "id": video.id,
                "description": video.description,
                "video_id": video.video_id,
                "title": video.title
            },
            "comments_analyzed": len(analyzed_comments),
            "comments": analyzed_comments
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
