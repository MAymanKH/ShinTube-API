from fastapi import APIRouter, HTTPException
from services.ytdlp_service import get_video_comments, get_video_info, get_video_subtitles
from utils import exceptions
from utils.logger import logger
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

router = APIRouter()

@router.get("/{video_id}")
async def videos(video_id: str):
    try:
        logger.info(f"Fetching info for video_id: {video_id}")
        video_info = await get_video_info(video_id)
        logger.info(f"Successfully fetched info for video_id: {video_id}")
        return video_info
    except exceptions.VideoNotFoundError as e:
        logger.error(f"Video not found for video_id: {video_id}, error: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except exceptions.YTDLPError as e:
        logger.error(f"Failed to fetch video info for video_id: {video_id}, error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch video info: {str(e)}")

@router.get("/{video_id}/comments")
async def video_comments(video_id: str):
    try:
        logger.info(f"Fetching comments for video_id: {video_id}")
        result = await get_video_comments(video_id)
        logger.info(f"Successfully fetched comments for video_id: {video_id}")
        return {"video_id": video_id, "result": result}
    except exceptions.VideoNotFoundError as e:
        logger.error(f"Video not found for comments for video_id: {video_id}, error: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except exceptions.DataParsingError as e:
        logger.error(f"Could not process comment data for video_id: {video_id}, error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: Could not process comment data. {e}")
    except exceptions.YTDLPError as e:
        logger.error(f"Failed to fetch comments for video_id: {video_id}, error: {e}")
        raise HTTPException(status_code=500, detail=f"Service Error: Failed to fetch comments. {e}")

@router.get("/{video_id}/subtitles")
async def video_subtitles(video_id: str):
    try:
        logger.info(f"Fetching subtitles for video_id: {video_id}")
        subtitles = await get_video_subtitles(video_id)
        logger.info(f"Successfully fetched subtitles for video_id: {video_id}")
        return {"video_id": video_id, "subtitles": subtitles}
    except exceptions.VideoNotFoundError as e:
        logger.error(f"Video not found for subtitles for video_id: {video_id}, error: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except exceptions.YTDLPError as e:
        logger.error(f"Failed to fetch subtitles for video_id: {video_id}, error: {e}")
        raise HTTPException(status_code=500, detail=f"Service Error: Failed to fetch subtitles. {e}")
