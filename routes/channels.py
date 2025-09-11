from fastapi import APIRouter, HTTPException
from services.ytdlp_service import get_channel_info, get_channel_videos
from utils import exceptions
from utils.logger import logger
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

router = APIRouter()

@router.get("/{channel_id}")
async def channels(channel_id: str):
    try:
        logger.info(f"Fetching info for channel_id: {channel_id}")
        channel_info = await get_channel_info(channel_id)
        logger.info(f"Successfully fetched info for channel_id: {channel_id}")
        return channel_info
    except exceptions.ChannelNotFoundError as e:
        logger.error(f"Channel not found for channel_id: {channel_id}, error: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except exceptions.YTDLPError as e:
        logger.error(f"Failed to fetch channel info for channel_id: {channel_id}, error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch channel info: {str(e)}")

@router.get("/{channel_id}/videos")
async def channel_videos(channel_id: str, limit: int = 100):
    try:
        logger.info(f"Fetching videos for channel_id: {channel_id} with limit: {limit}")
        videos = await get_channel_videos(channel_id, limit)
        logger.info(f"Successfully fetched videos for channel_id: {channel_id}")
        return {"channel_id": channel_id, "videos": videos}
    except exceptions.ChannelNotFoundError as e:
        logger.error(f"Channel not found for videos for channel_id: {channel_id}, error: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except exceptions.YTDLPError as e:
        logger.error(f"Failed to fetch videos for channel_id: {channel_id}, error: {e}")
        raise HTTPException(status_code=500, detail=f"Service Error: Failed to fetch videos. {e}")
