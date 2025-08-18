from typing import Dict, List, Any
from datetime import datetime


async def format_duration(seconds):
    if not seconds:
        return None
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    if h:
        return f"{h}:{m:02}:{s:02}"
    else:
        return f"{m}:{s:02}"


async def format_number(n):
    if n is None:
        return None
    return f"{n:,}"


async def format_compact_number(n):
    if n is None:
        return None
    n = int(n)
    if n >= 1_000_000_000:
        return f"{n/1_000_000_000:.1f}B"
    elif n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    elif n >= 1_000:
        return f"{n/1_000:.1f}K"
    else:
        return str(n)


async def format_date(date_str):
    if not date_str:
        return None
    try:
        dt = datetime.strptime(date_str, "%Y%m%d")
        return dt.strftime("%b %d, %Y")
    except Exception:
        return date_str


async def format_relative_time(upload_date: str, release_year: int = None) -> str:
    if not upload_date and release_year:
        try:
            current_year = datetime.now().year
            year_diff = current_year - release_year
            if year_diff <= 0:
                return "This year"
            elif year_diff == 1:
                return "Last year"
            else:
                return f"{year_diff} years ago"
        except:
            return "Unknown"
    if not upload_date:
        return "Unknown"
    try:
        upload_dt = datetime.strptime(upload_date, "%Y%m%d")
        now = datetime.now()
        diff = now - upload_dt
        days = diff.days
        if days < 0: return "In the future"
        if days == 0:
            return "Today"
        elif days == 1:
            return "Yesterday"
        elif days < 7:
            return f"{days} days ago"
        elif days < 30:
            weeks = days // 7
            return f"{weeks} week{'s' if weeks > 1 else ''} ago"
        elif days < 365:
            months = days // 30
            return f"{months} month{'s' if months > 1 else ''} ago"
        else:
            years = days // 365
            return f"{years} year{'s' if years > 1 else ''} ago"
    except:
        return "Unknown"


async def format_video_info(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    # Select one high quality thumbnail url
    thumbnail_url = None
    if raw_data.get("thumbnails"):
        sorted_thumbs = sorted(raw_data["thumbnails"], key=lambda t: t.get("width", 0), reverse=True)
        thumbnail_url = sorted_thumbs[0].get("url") if sorted_thumbs else None

    return {
        "id": raw_data.get("id"),
        "title": raw_data.get("title"),
        "description": raw_data.get("description"),
        "channel": raw_data.get("channel"),
        "channel_id": raw_data.get("channel_id"),
        "channel_url": raw_data.get("channel_url"),
        "channel_follower_count": raw_data.get("channel_follower_count"),
        "channel_follower_count_string": await format_number(raw_data.get("channel_follower_count")),
        "channel_follower_count_compact_string": await format_compact_number(raw_data.get("channel_follower_count")),
        "uploader": raw_data.get("uploader"),
        "uploader_id": raw_data.get("uploader_id"),
        "duration": raw_data.get("duration"),
        "duration_string": await format_duration(raw_data.get("duration")),
        "view_count": raw_data.get("view_count"),
        "view_count_string": await format_number(raw_data.get("view_count")),
        "view_count_compact_string": await format_compact_number(raw_data.get("view_count")),
        "like_count": raw_data.get("like_count"),
        "like_count_string": await format_number(raw_data.get("like_count")),
        "like_count_compact_string": await format_compact_number(raw_data.get("like_count")),
        "publish_date": raw_data.get("upload_date"),
        "publish_date_string": await format_date(raw_data.get("upload_date")),
        "thumbnail_url": thumbnail_url,
        "webpage_url": raw_data.get("webpage_url"),
    }


async def format_playlist_info(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    entries = []
    if raw_data.get('entries'):
        for entry in raw_data['entries']:
            if entry:
                entries.append({
                    'video_id': entry.get('id'),
                    'title': entry.get('title'),
                    'uploader': entry.get('uploader'),
                    'duration': entry.get('duration'),
                    'url': entry.get('url') or entry.get('webpage_url')
                })
    return {
        'playlist_id': raw_data.get('id'),
        'title': raw_data.get('title'),
        'description': raw_data.get('description'),
        'uploader': raw_data.get('uploader') or raw_data.get('channel'),
        'item_count': raw_data.get('playlist_count') or len(entries),
        'videos': entries,
        'webpage_url': raw_data.get('webpage_url')
    }


async def   format_search_results(raw_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    formatted_results = []
    for result in raw_results:
        upload_date = result.get('upload_date')
        view_count = result.get('view_count')
        duration = result.get('duration')
        video_id = result.get('id')
        thumbnails = []
        if video_id:
            thumbnails = [
                {
                    'url': f"https://img.youtube.com/vi/{video_id}/mqdefault.jpg",
                    'width': 320,
                    'height': 180,
                    'resolution': '320x180'
                },
                {
                    'url': f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg",
                    'width': 480,
                    'height': 360,
                    'resolution': '480x360'
                }
            ]
        if result.get('thumbnails'):
            existing_thumbnails = []
            for thumb in result['thumbnails']:
                if thumb.get('url'):
                    width = thumb.get('width')
                    height = thumb.get('height')
                    existing_thumbnails.append({
                        'url': thumb['url'],
                        'width': width,
                        'height': height,
                        'resolution': f"{width}x{height}" if width and height else "unknown"
                    })
            if existing_thumbnails:
                thumbnails = existing_thumbnails[:2]
        formatted_results.append({
            'video_id': video_id,
            'title': result.get('title'),
            'uploader': result.get('uploader') or result.get('channel') or result.get('channel_id'),
            'duration': duration,
            'duration_string': await format_duration(duration),
            'view_count': view_count,
            'view_count_string': await format_compact_number(view_count) if view_count else "Unknown views",
            'upload_date': upload_date,
            'upload_date_string': await format_relative_time(upload_date) if upload_date else "Unknown",
            'thumbnails': thumbnails,
            'url': result.get('url') or f"https://youtube.com/watch?v={video_id}" if video_id else None
        })
    return formatted_results