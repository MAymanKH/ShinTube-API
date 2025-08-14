from fastapi import APIRouter, HTTPException, Query, BackgroundTasks
from fastapi.responses import FileResponse
import sys
import os

# Add parent directory to path to import services
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services import ytdlp_service

router = APIRouter()

def cleanup_file(file_path: str):
    """Background task to cleanup downloaded file"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception:
        pass  # Silently fail cleanup

@router.get("/{video_id}")
async def download(
    video_id: str,
    background_tasks: BackgroundTasks,
    format: str = Query(None, description="Format ID for download")
):
    try:
        file_info = await ytdlp_service.download_video(video_id, format)
        
        # Schedule cleanup after file is sent
        background_tasks.add_task(cleanup_file, file_info["file_path"])
        
        return FileResponse(
            path=file_info["file_path"],
            filename=file_info["filename"],
            media_type="application/octet-stream"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")
