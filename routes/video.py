from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from services import ytdlp_service
from utils.format_parser import format_duration, format_number, format_compact_number, format_date
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
        # If yt-dlp returns an error or missing info
        if not info or 'title' not in info:
            raise HTTPException(status_code=404, detail="Video not found")
        # Select one high quality thumbnail url
        thumbnail_url = None
        if info.get("thumbnails"):
            sorted_thumbs = sorted(info["thumbnails"], key=lambda t: t.get("width", 0), reverse=True)
            thumbnail_url = sorted_thumbs[0].get("url") if sorted_thumbs else None
        # Clean up the response: select relevant fields
        result = {
            "id": info.get("id"),
            "title": info.get("title"),
            "description": info.get("description"),
            "channel": info.get("channel"),
            "channel_id": info.get("channel_id"),
            "channel_url": info.get("channel_url"),
            "channel_follower_count": info.get("channel_follower_count"),
            "channel_follower_count_string": await format_number(info.get("channel_follower_count")),
            "channel_follower_count_compact_string": await format_compact_number(info.get("channel_follower_count")),
            "uploader": info.get("uploader"),
            "uploader_id": info.get("uploader_id"),
            "duration": info.get("duration"),
            "duration_string": await format_duration(info.get("duration")),
            "view_count": info.get("view_count"),
            "view_count_string": await format_number(info.get("view_count")),
            "view_count_compact_string": await format_compact_number(info.get("view_count")),
            "like_count": info.get("like_count"),
            "like_count_string": await format_number(info.get("like_count")),
            "like_count_compact_string": await format_compact_number(info.get("like_count")),
            "publish_date": info.get("upload_date"),
            "publish_date_string": await format_date(info.get("upload_date")),
            "thumbnail_url": thumbnail_url,
            "webpage_url": info.get("webpage_url"),
        }
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch video info: {str(e)}")