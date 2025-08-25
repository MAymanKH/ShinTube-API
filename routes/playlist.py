from fastapi import APIRouter, HTTPException
from services import ytdlp_service
from utils import exceptions
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

router = APIRouter()

@router.get("/{playlist_id}")
async def get_playlist(playlist_id: str):
    try:
        playlist_info = await ytdlp_service.get_playlist_info(playlist_id)
        return playlist_info
    except exceptions.PlaylistNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except exceptions.YTDLPError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch playlist: {str(e)}")