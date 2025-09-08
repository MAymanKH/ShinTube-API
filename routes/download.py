from fastapi import APIRouter, HTTPException, Query, BackgroundTasks
from fastapi.responses import FileResponse
from services import ytdlp_service
from utils.logger import get_logger
import sys
import os

# Add parent directory to path to import services
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

router = APIRouter()
logger = get_logger(__name__)

def cleanup_file(file_path: str):
    """Background task to cleanup downloaded file"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Cleaned up file: {file_path}")
    except Exception as e:
        logger.error(f"Failed to cleanup file: {file_path}, error: {e}")

@router.get("/{video_id}")
async def download(
    video_id: str,
    background_tasks: BackgroundTasks,
    format: str = Query(None, description="Format ID for download")
):
    try:
        logger.info(f"Downloading video_id: {video_id} with format: {format}")
        file_info = await ytdlp_service.download_video(video_id, format)
        
        # Schedule cleanup after file is sent
        background_tasks.add_task(cleanup_file, file_info["file_path"])
        
        logger.info(f"Sending file: {file_info['filename']}")
        return FileResponse(
            path=file_info["file_path"],
            filename=file_info["filename"],
            media_type="application/octet-stream"
        )
    except Exception as e:
        logger.error(f"Download failed for video_id: {video_id}, error: {e}")
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")
