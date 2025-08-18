from fastapi import APIRouter, Query, HTTPException
from services import ytdlp_service
from utils.format_parser import format_video_info
from typing import Optional
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

router = APIRouter()

@router.get("/{video_id}")
async def video(video_id: str):
    if not video_id:
        raise HTTPException(status_code=422, detail="Query parameter 'video_id' is required")

    try:
        info = await ytdlp_service.get_video_info(video_id)
        if not info or 'title' not in info:
            raise HTTPException(status_code=404, detail="Video not found")
        result = await format_video_info(info)
        return {"video_id": video_id, "result": result}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch video info: {str(e)}")