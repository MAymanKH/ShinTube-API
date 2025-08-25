from fastapi import APIRouter, HTTPException
from services.ytdlp_service import get_video_comments, get_video_info
from utils import exceptions
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

router = APIRouter()

@router.get("/{video_id}")
async def videos(video_id: str):
    try:
        video_info = await get_video_info(video_id)
        return video_info
    except exceptions.VideoNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except exceptions.YTDLPError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch video info: {str(e)}")

@router.get("/{video_id}/comments")
async def video_comments(video_id: str):
    try:
        result = await get_video_comments(video_id)
        return {"video_id": video_id, "result": result}
    except exceptions.VideoNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except exceptions.DataParsingError as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: Could not process comment data. {e}")
    except exceptions.YTDLPError as e:
        raise HTTPException(status_code=500, detail=f"Service Error: Failed to fetch comments. {e}")