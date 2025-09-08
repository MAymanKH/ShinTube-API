from fastapi import APIRouter, HTTPException
from services.ytdlp_service import get_playlist_info
from utils import exceptions
from utils.logger import logger
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

router = APIRouter()

@router.get("/{playlist_id}")
async def playlists(playlist_id: str):
    try:
        logger.info(f"Fetching playlist_id: {playlist_id}")
        playlist_info = await get_playlist_info(playlist_id)
        logger.info(f"Successfully fetched playlist_id: {playlist_id}")
        return playlist_info
    except exceptions.PlaylistNotFoundError as e:
        logger.error(f"Playlist not found for playlist_id: {playlist_id}, error: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except exceptions.YTDLPError as e:
        logger.error(f"Failed to fetch playlist for playlist_id: {playlist_id}, error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch playlist: {str(e)}")
