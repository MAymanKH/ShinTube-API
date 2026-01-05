from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import StreamingResponse
from services.ytdlp_service import get_video_comments, get_video_info, get_video_subtitles, get_video_formats, get_video_stream
from utils import exceptions
from utils.format_parser import format_download_filename
from utils.logger import logger
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

router = APIRouter()

@router.get("/{video_id}")
async def videos(request: Request, video_id: str):
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
async def video_comments(request: Request, video_id: str):
    try:
        logger.info(f"Fetching comments for video_id: {video_id}")
        result = await get_video_comments(video_id, 50, 500)
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
async def video_subtitles(request: Request, video_id: str):
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

@router.get("/{video_id}/formats")
async def video_formats(request: Request, video_id: str, type: str = Query("all", enum=["all", "video", "audio", "merged"], description="Filter formats by type: 'audio' (audio only), 'video' (any video format), 'merged' (video+audio), or 'all'")):
    try:
        logger.info(f"Fetching formats for video_id: {video_id} with filter: {type}")
        formats = await get_video_formats(video_id, type)
        logger.info(f"Successfully fetched formats for video_id: {video_id}")
        return {"video_id": video_id, "formats": formats}
    except exceptions.VideoNotFoundError as e:
        logger.error(f"Video not found for formats for video_id: {video_id}, error: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except exceptions.YTDLPError as e:
        logger.error(f"Failed to fetch formats for video_id: {video_id}, error: {e}")
        raise HTTPException(status_code=500, detail=f"Service Error: Failed to fetch formats. {e}")

@router.get("/{video_id}/download")
async def download_video(request: Request, video_id: str, format_id: str = Query("b", description="The format ID to download")):
    try:
        logger.info(f"Starting download stream for video_id: {video_id}, format_id: {format_id}")
        # Fetch video info for title
        video_info = await get_video_info(video_id)
        title = video_info.get("title", video_id)
        formats = []
        if format_id != "b": formats = await get_video_formats(video_id)
        filename = await format_download_filename(title, format_id, formats)
        stream_generator = get_video_stream(video_id, format_id)
        return StreamingResponse(
            stream_generator,
            media_type="application/octet-stream",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'}
        )
    except Exception as e:
        logger.error(f"Failed to start download stream for video_id: {video_id}, error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to start download stream: {e}")
