# app/services/video_service.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.video_model import Video

async def get_or_create_video(db: AsyncSession, video_id: str, title: str = None, description: str = None) -> Video:
    """
    Busca un video en la base de datos por su video_id.
    Si no existe, lo crea con title y description.
    Si existe y title o description están vacíos, los actualiza.
    """
    result = await db.execute(select(Video).filter(Video.video_id == video_id))
    video = result.scalars().first()

    if video is None:
        # Crear el video con title y description
        video = Video(video_id=video_id, title=title, description=description)
        db.add(video)
        await db.commit()
        await db.refresh(video)
    else:
        # Si el video ya existe pero no tiene título o descripción, las actualizamos si tenemos datos
        updated = False
        if title and (video.title is None or video.title.strip() == ""):
            video.title = title
            updated = True
        if description and (video.description is None or video.description.strip() == ""):
            video.description = description
            updated = True
        
        if updated:
            await db.commit()
            await db.refresh(video)

    return video
