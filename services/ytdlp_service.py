import asyncio
import os
import tempfile
import subprocess
import json
import sys
from typing import List, Dict, Any

from fastapi import HTTPException
from utils.format_parser import format_comments, format_search_results, format_video_info, format_playlist_info
from utils import exceptions
from utils.logger import get_logger

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
logger = get_logger(__name__)

async def run_ytdlp_process(args: List[str]):
    """Helper function to execute the yt-dlp process and handle its output."""
    cmd = ["yt-dlp"] + args
    logger.debug(f"Running yt-dlp command: {' '.join(cmd)}")
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    
    if process.returncode != 0:
        error_message = stderr.decode().strip()
        logger.error(f"yt-dlp failed with exit code {process.returncode}: {error_message}")
        if "Video unavailable" in error_message or "Private video" in error_message:
            raise exceptions.VideoNotFoundError(error_message)
        if "playlist does not exist" in error_message:
            raise exceptions.PlaylistNotFoundError(error_message)
        raise exceptions.YTDLPError(f"yt-dlp failed: {error_message}")
        
    logger.debug("yt-dlp process finished successfully.")
    return stdout.decode()

async def search_videos(query: str, limit: int = 15) -> List[Dict[str, Any]]:
    args = [
        f"ytsearch{limit}:{query}",
        "--dump-json",
        "--flat-playlist",
        "--no-download",
        "--no-warnings",
        "--quiet",
        "--extractor-args",
        "youtubetab:approximate_date"
    ]
    try:
        output = await run_ytdlp_process(args)
        videos = [json.loads(line) for line in output.strip().split('\n') if line]
        return await format_search_results(videos)
    except json.JSONDecodeError as e:
        raise exceptions.YTDLPError(f"Failed to parse search results: {e}")

async def get_video_info(video_id: str) -> Dict[str, Any]:
    args = [
        f"https://youtube.com/watch?v={video_id}",
        "--dump-json",
        "--no-download",
        "--skip-download",
        "--no-playlist",
        "--ignore-errors"
    ]
    try:
        output = await run_ytdlp_process(args)
        if not output.strip():
            raise exceptions.VideoNotFoundError(f"No metadata found for video_id: {video_id}")
        info = json.loads(output)
        return await format_video_info(info)
    except json.JSONDecodeError:
        raise exceptions.VideoNotFoundError(f"Could not parse video metadata for ID: {video_id}. It may be unavailable.")

async def get_playlist_info(playlist_id: str) -> Dict[str, Any]:
    """Get playlist information and video list"""
    args = [
        f"https://youtube.com/playlist?list={playlist_id}",
        "--dump-json",
        "--no-download",
        "--flat-playlist"
    ]
    
    output = await run_ytdlp_process(args)
    
    # Get all lines of output, filtering out empty ones
    lines = [line for line in output.strip().split('\n') if line]
    
    # If there are no lines, the playlist is empty or private
    if not lines:
        raise exceptions.PlaylistNotFoundError(f"Playlist '{playlist_id}' is empty, private, or does not exist.")

    # Convert all lines to JSON objects
    video_entries = [json.loads(line) for line in lines]
    
    # Extract the common playlist metadata from the FIRST video entry.
    first_video = video_entries[0]
    playlist_metadata = {
        'id': first_video.get('playlist_id'),
        'title': first_video.get('playlist_title'),
        'uploader': first_video.get('playlist_uploader'),
        'channel_id': first_video.get('playlist_uploader_id'),
        'channel_url': first_video.get('playlist_uploader_url'),
        'playlist_count': len(video_entries), # Count the actual entries we received
        'webpage_url': first_video.get('playlist_webpage_url')
    }

    return await format_playlist_info(playlist_metadata, video_entries)

# The download_video function remains unchanged as it doesn't format JSON output
async def download_video(video_id: str, format_id: str = None) -> Dict[str, Any]:
    temp_dir = tempfile.gettempdir()
    output_template = os.path.join(temp_dir, f"{video_id}.%(ext)s")
    
    args = [f"https://youtube.com/watch?v={video_id}", "--output", output_template]
    if format_id:
        args.extend(["-f", format_id])
    
    try:
        await run_ytdlp_process(args)
        for file in os.listdir(temp_dir):
            if file.startswith(video_id):
                file_path = os.path.join(temp_dir, file)
                return {
                    "file_path": file_path, "filename": file,
                    "video_id": video_id, "format_id": format_id
                }
        raise exceptions.DownloadError("Download completed but the file was not found.")
    except exceptions.YTDLPError as e:
        raise exceptions.DownloadError(f"Download failed: {str(e)}")

async def get_video_comments(video_id: str, limit: int = 600, sort_by: str = "top") -> Dict[str, Any]:
    """Get video comments using yt-dlp."""
    extractor_args_string = f"youtube:max_comments={limit};comment_sort={sort_by};comment_mode=all"
    args = [
        f"https://youtube.com/watch?v={video_id}",
        "--get-comments",
        "--extractor-args",
        extractor_args_string,
        "--dump-json",
        "--no-download",
        "--skip-download",
    ]

    try:
        output = await run_ytdlp_process(args)
        data = json.loads(output)
        raw_comments = data.get('comments')
        if raw_comments is None:
            return await format_comments([], limit) 
        return await format_comments(raw_comments, limit)
    except json.JSONDecodeError:
        raise exceptions.DataParsingError(f"Could not parse comment data for video ID: {video_id}.")
