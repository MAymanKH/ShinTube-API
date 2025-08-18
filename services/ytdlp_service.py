import asyncio
import os
import tempfile
import subprocess
import json
import sys
from typing import List, Dict, Any
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.format_parser import format_search_results


async def run_ytdlp(args: List[str]) -> Dict[str, Any]:
    """
    Execute yt-dlp command and return JSON output
    
    Args:
        args: List of yt-dlp command arguments
        
    Returns:
        Dictionary containing yt-dlp output
    """
    try:
        cmd = ["yt-dlp"] + args
        result = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = await result.communicate()
        
        # Try to parse JSON even if returncode != 0 (yt-dlp may still output metadata)
        try:
            return json.loads(stdout.decode())
        except json.JSONDecodeError:
            # Handle non-JSON output
            if result.returncode != 0:
                raise Exception(f"yt-dlp failed: {stderr.decode()}")
            return {"output": stdout.decode() if stdout else ""}
    except Exception as e:
        raise Exception(f"Failed to execute yt-dlp: {str(e)}")


async def search_videos(query: str, limit: int = 15) -> List[Dict[str, Any]]:
    """
    Search for videos using yt-dlp
    
    Args:
        query: Search query string
        limit: Maximum number of results to return
        
    Returns:
        List of video information dictionaries
    """
    args = [
        f"ytsearch{limit}:{query}",
        "--dump-json",
        "--flat-playlist",
        "--no-download",
        "--no-warnings",
        "--quiet",
        "--extractor-args", "youtubetab:approximate_date"
    ]
    
    try:
        cmd = ["yt-dlp"] + args
        result = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = await result.communicate()
        
        if result.returncode != 0:
            raise Exception(f"Search failed: {stderr.decode()}")
        
        # Parse multiple JSON objects
        videos = []
        for line in stdout.decode().strip().split('\n'):
            if line:
                try:
                    videos.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        
        return await format_search_results(videos)
    except Exception as e:
        raise Exception(f"Search failed: {str(e)}")


async def get_video_info(video_id: str) -> Dict[str, Any]:
    """
    Get video information
    
    Args:
        video_id: YouTube video ID
        
    Returns:
        Dictionary containing video metadata
    """
    args = [
        f"https://youtube.com/watch?v={video_id}",
        "--dump-json",
        "--no-download",
        "--skip-download",
        "--no-playlist",
        "--ignore-errors"    # Continue even if some formats fail
    ]
    
    return await run_ytdlp(args)


async def get_playlist_info(playlist_id: str) -> Dict[str, Any]:
    """
    Get playlist information and video list
    
    Args:
        playlist_id: YouTube playlist ID
        
    Returns:
        Dictionary containing playlist metadata and videos
    """
    args = [
        f"https://youtube.com/playlist?list={playlist_id}",
        "--dump-json",
        "--no-download",
        "--flat-playlist"
    ]
    
    try:
        cmd = ["yt-dlp"] + args
        result = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = await result.communicate()
        
        if result.returncode != 0:
            raise Exception(f"Playlist fetch failed: {stderr.decode()}")
        
        # Parse playlist entries
        videos = []
        playlist_info = None
        
        for line in stdout.decode().strip().split('\n'):
            if line:
                data = json.loads(line)
                if data.get('_type') == 'playlist':
                    playlist_info = data
                else:
                    videos.append(data)
        
        return {
            "playlist_id": playlist_id,
            "title": playlist_info.get('title', 'Unknown Playlist') if playlist_info else 'Unknown Playlist',
            "uploader": playlist_info.get('uploader', 'Unknown') if playlist_info else 'Unknown',
            "item_count": len(videos),
            "videos": videos
        }
    except Exception as e:
        raise Exception(f"Failed to fetch playlist: {str(e)}")


async def download_video(video_id: str, format_id: str = None) -> Dict[str, Any]:
    """
    Download video temporarily for streaming
    
    Args:
        video_id: YouTube video ID
        format_id: Optional format ID for specific quality
        
    Returns:
        Dictionary containing file path and metadata
    """
    temp_dir = tempfile.gettempdir()
    output_template = os.path.join(temp_dir, f"{video_id}.%(ext)s")
    
    args = [
        f"https://youtube.com/watch?v={video_id}",
        "--output", output_template
    ]
    
    if format_id:
        args.extend(["-f", format_id])
    
    try:
        cmd = ["yt-dlp"] + args
        result = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = await result.communicate()
        
        if result.returncode != 0:
            raise Exception(f"Download failed: {stderr.decode()}")
        
        # Find the downloaded file
        for file in os.listdir(temp_dir):
            if file.startswith(video_id):
                file_path = os.path.join(temp_dir, file)
                return {
                    "file_path": file_path,
                    "filename": file,
                    "video_id": video_id,
                    "format_id": format_id
                }
        
        raise Exception("Downloaded file not found")
    except Exception as e:
        raise Exception(f"Download failed: {str(e)}")
    except Exception as e:
        raise Exception(f"Download failed: {str(e)}")
    except Exception as e:
        raise Exception(f"Download failed: {str(e)}")
