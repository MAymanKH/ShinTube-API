from typing import Dict, List, Any
from datetime import datetime

# --- Start of Helper Functions ---

def format_duration(seconds):
    if seconds is None:
        return None
    try:
        s = int(seconds)
        m, s = divmod(s, 60)
        h, m = divmod(m, 60)
        return f"{h}:{m:02}:{s:02}" if h else f"{m}:{s:02}"
    except (ValueError, TypeError):
        return None

def format_number(n):
    if n is None:
        return None
    return f"{n:,}"

def format_compact_number(n):
    if n is None:
        return None
    try:
        n = int(n)
        if n >= 1_000_000_000:
            return f"{n/1_000_000_000:.1f}B"
        if n >= 1_000_000:
            return f"{n/1_000_000:.1f}M"
        if n >= 1_000:
            return f"{n/1_000:.1f}K"
        return str(n)
    except (ValueError, TypeError):
        return str(n)

def format_date(date_str):
    if not date_str:
        return None
    try:
        dt = datetime.strptime(date_str, "%Y%m%d")
        return dt.strftime("%b %d, %Y")
    except (ValueError, TypeError):
        return date_str

def format_relative_time(upload_date: str) -> str:
    if not upload_date:
        return "Unknown"
    try:
        upload_dt = datetime.strptime(upload_date, "%Y%m%d")
        now = datetime.now()
        diff = now - upload_dt
        days = diff.days

        if days < 0: return "In the future"
        if days == 0: return "Today"
        if days == 1: return "Yesterday"
        if days < 7: return f"{days} days ago"
        if days < 30:
            weeks = days // 7
            return f"{weeks} week{'s' if weeks > 1 else ''} ago"
        if days < 365:
            months = days // 30
            return f"{months} month{'s' if months > 1 else ''} ago"
        
        years = days // 365
        return f"{years} year{'s' if years > 1 else ''} ago"
    except (ValueError, TypeError):
        return "Unknown"

# ----------------------------------

async def format_search_results(raw_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    formatted_results = []
    for result in raw_results:
        video_id = result.get('id')
        thumbnails = [
            {'url': f"https://img.youtube.com/vi/{video_id}/mqdefault.jpg", 'width': 320, 'height': 180, 'resolution': "320x180"},
            {'url': f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg", 'width': 480, 'height': 360, 'resolution': "480x360"},
        ]

        formatted_results.append({
            'video_id': video_id,
            'url': result.get('url'),
            'title': result.get('title'),
            'live_status': result.get('live_status'),
            'uploader': result.get('uploader') or result.get('channel'),
            'duration': result.get('duration'),
            'duration_string': format_duration(result.get('duration')),
            'view_count': result.get('view_count'),
            'view_count_string': format_compact_number(result.get('view_count')),
            'upload_date': result.get('upload_date'),
            'upload_date_string': format_relative_time(result.get('upload_date')),
            'thumbnails': thumbnails,
        })
    return formatted_results

async def format_video_info(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    video_id = raw_data.get("id")
    thumbnails = [
                {'url': f"https://img.youtube.com/vi/{video_id}/mqdefault.jpg", 'width': 320, 'height': 180, 'resolution': "320x180"},
                {'url': f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg", 'width': 480, 'height': 360, 'resolution': "480x360"},
                {'url': f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg", 'width': 1280, 'height': 720, 'resolution': "1280x720"}
            ]

    return {
        "video_id": video_id,
        "url": raw_data.get("webpage_url"),
        "title": raw_data.get("title"),
        "description": raw_data.get("description"),
        "channel": raw_data.get("channel"),
        "channel_id": raw_data.get("channel_id"),
        "channel_url": raw_data.get("channel_url"),
        "channel_follower_count": raw_data.get("channel_follower_count"),
        "channel_follower_count_string": format_number(raw_data.get("channel_follower_count")),
        "channel_follower_count_compact_string": format_compact_number(raw_data.get("channel_follower_count")),
        "uploader": raw_data.get("uploader"),
        "duration": raw_data.get("duration"),
        "duration_string": format_duration(raw_data.get("duration")),
        "view_count": raw_data.get("view_count"),
        "view_count_string": format_number(raw_data.get("view_count")),
        "view_count_compact_string": format_compact_number(raw_data.get("view_count")),
        "like_count": raw_data.get("like_count"),
        "like_count_string": format_number(raw_data.get("like_count")),
        "like_count_compact_string": format_compact_number(raw_data.get("like_count")),
        "publish_date": raw_data.get("upload_date"),
        "publish_date_string": format_date(raw_data.get("upload_date")),
        "relative_publish_date": format_relative_time(raw_data.get("upload_date")),
        "thumbnails": thumbnails,
    }

async def format_playlist_info(playlist_data: Dict[str, Any], video_entries: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Formats the playlist metadata and its list of videos."""
    channel_id = playlist_data.get('channel_id')
    channel_url = playlist_data.get('channel_url')
    if not channel_url and channel_id:
        if channel_id.startswith('@'): channel_url = f"https://www.youtube.com/{playlist_data.get('channel_id')}"
        else: channel_url = f"https://www.youtube.com/channel/{playlist_data.get('channel_id')}"
    return {
        'playlist_id': playlist_data.get('id'),
        'title': playlist_data.get('title'),
        'description': playlist_data.get('description'),
        'uploader': playlist_data.get('uploader') or playlist_data.get('channel'),
        'channel_id': channel_id,
        'channel_url': channel_url,
        'item_count': playlist_data.get('playlist_count') or len(video_entries),
        'videos': await format_search_results(video_entries), # Reuse the search formatter
        'webpage_url': playlist_data.get('webpage_url')
    }