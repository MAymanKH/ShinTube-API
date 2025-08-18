from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from services import ytdlp_service
from utils.format_parser import format_video_info
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

router = APIRouter()

@router.get("/video/{video_id}")
async def video(video_id: str):
    if not video_id:
        raise HTTPException(status_code=422, detail="Query parameter 'video_id' is required")

    try:
        info = await ytdlp_service.get_video_info(video_id)
        if not info or 'title' not in info:
            raise HTTPException(status_code=404, detail="Video not found")
        result = await format_video_info(info)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch video info: {str(e)}")