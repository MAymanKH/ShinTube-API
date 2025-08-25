from fastapi import APIRouter, Query, HTTPException
from services.ytdlp_service import get_video_info
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

router = APIRouter()

@router.get("/")
async def video(video_id: str = Query(..., description="The ID of the video to fetch.")):

    try:
        result = await get_video_info(video_id)
        return {"video_id": video_id, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch video info: {str(e)}")