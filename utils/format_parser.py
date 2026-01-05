import json
import re
from typing import Dict, List, Any
from datetime import datetime
from .logger import logger


# --- Start of Helper Functions ---

def format_duration(seconds):
    if seconds is None:
        return None
    try:
        s = int(seconds)
        m, s = divmod(s, 60)
        h, m = divmod(m, 60)
        return f"{h}:{m:02}:{s:02}" if h else f"{m}:{s:02}"
    except (ValueError, TypeError) as e:
        logger.error(f"Could not format duration for value: {seconds}. Error: {e}")
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
    except (ValueError, TypeError) as e:
        logger.error(f"Could not format compact number for value: {n}. Error: {e}")
        return str(n)

def format_date(date_str):
    if not date_str:
        return None
    try:
        dt = datetime.strptime(date_str, "%Y%m%d")
        return dt.strftime("%b %d, %Y")
    except (ValueError, TypeError) as e:
        logger.error(f"Could not format date for value: {date_str}. Error: {e}")
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
    except (ValueError, TypeError) as e:
        logger.error(f"Could not format relative time for value: {upload_date}. Error: {e}")
        return "Unknown"

# ----------------------------------

# Formats `/search/q={query}` output
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

# Formats `/search/q={query}&type=playlist` output
async def format_playlist_search_results(raw_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    formatted_results = []
    for result in raw_results:
        playlist_id = result.get('id')
        thumbnails = result.get('thumbnails', [])

        formatted_results.append({
            'playlist_id': playlist_id,
            'url': result.get('url'),
            'title': result.get('title'),
            'uploader': result.get('uploader') or result.get('channel'),
            'video_count': result.get('playlist_count'),
            'thumbnails': thumbnails,
        })
    return formatted_results

# Formats `/videos/{video_id}` output
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

# Formats `/playlists/{playlist_id}` output
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

# Formats `/videos/{video_id}/comments` output
async def format_comments(raw_comments: List[Dict[str, Any]], limit: int) -> Dict[str, Any]:
    """
    Formats raw comments, nests replies under their parents, and applies a limit
    only to the root-level comments.
    """
    comment_map = {}
    root_comments = []

    # First, process all comments into a structured map.
    for comment in raw_comments:
        comment_id = comment.get('id')
        if not comment_id:
            continue
        
        author = comment.get('author') or 'Unknown'
        author_id = comment.get('author_id')
        author_url = None
        if author_id and author_id.startswith('UC'):
            author_url = f"https://www.youtube.com/channel/{author_id}"
        elif author_id:
            author_url = f"https://www.youtube.com/{author_id}"
            
        comment_map[comment_id] = {
            "comment_id": comment_id,
            "text": comment.get('text'),
            "author": author,
            "author_id": author_id,
            "author_url": author_url,
            "like_count": comment.get('like_count'),
            "like_count_string": format_compact_number(comment.get('like_count')),
            "is_hearted": comment.get('is_favorited', False),
            "is_pinned": comment.get('is_pinned', False),
            "timestamp": comment.get('timestamp'),
            "time_text": comment.get('_time_text'),
            "parent_id": comment.get('parent'),
            "reply_count": 0,
            "replies": []
        }

    # Separate root comments from replies and nest replies under their parents.
    for comment_id, comment_data in comment_map.items():
        parent_id = comment_data.pop('parent_id', None)
        
        if parent_id and parent_id in comment_map:
            parent_comment = comment_map[parent_id]
            parent_comment['replies'].append(comment_data)
            parent_comment['reply_count'] += 1
        else:
            root_comments.append(comment_data)

    # Sort replies within each root comment by likes (most liked first).
    for comment in root_comments:
        if comment['replies']:
            comment['replies'].sort(key=lambda r: r.get('like_count', 0), reverse=True)

    # Sort root comments: pinned comments first, then by likes (most liked first).
    root_comments.sort(key=lambda c: (c.get('is_pinned', False), c.get('like_count', 0)), reverse=True)

    # Apply the limit to the list of root comments.
    limited_root_comments = root_comments[:limit]

    return {
        "comment_count": len(limited_root_comments),
        "comments": limited_root_comments
    }

# Formats `/videos/{video_id}/subtitles` output
async def format_subtitles(raw_subtitles: str) -> List[Dict[str, Any]]:
    """Formats the JSON subtitles output from yt-dlp into unique tracks with download URLs.
    Returns an empty list if no valid data exists.
    """
    if not raw_subtitles or not raw_subtitles.strip(): return []
    try: subs = json.loads(raw_subtitles.strip())
    except (json.JSONDecodeError, TypeError): return []

    if not isinstance(subs, dict) or not subs: return []

    subtitles = []
    for lang_code, tracks in subs.items():
        # Skip auto-translated (yt-dlp marks them like "xx-yy") and live chat
        if "-" in lang_code or lang_code == "live_chat": continue
        # Collect formats with URLs
        formats = []
        is_auto = False
        for track in tracks:
            ext = track.get("ext")
            url = track.get("url")
            if not ext or not url: continue
            formats.append({"ext": ext, "url": url})
            if track.get("auto", False): is_auto = True
        if not formats: continue

        # Pick a human-friendly name (e.g. "English")
        base_name = tracks[0].get("name") or lang_code
        if is_auto and not base_name.lower().endswith("(auto-generated)"): name = f"{base_name} (auto-generated)"
        else: name = base_name

        subtitles.append({
            "language_code": lang_code,
            "language_name": name,
            "is_auto_generated": is_auto,
            "is_auto_translated": False,
            "formats": formats,  # list of {ext, url}
        })

    return subtitles or []

# Formats `/channels/{channel_id}` output
async def format_channel_info(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """Formats the channel metadata."""
    raw_thumbnails = raw_data.get("thumbnails", [])
    banners = []
    avatars = []
    if raw_thumbnails:
        for thumb in raw_thumbnails:
            thumb_id = thumb.get("id", "")
            height = thumb.get("height")
            width = thumb.get("width")
            if 'avatar' in thumb_id or (height and width and height == width): avatars.append(thumb)
            elif 'banner' in thumb_id or (height and width and width > height): banners.append(thumb)

    return {
        "channel_id": raw_data.get("channel_id"),
        "channel_url": raw_data.get("channel_url"),
        "title": raw_data.get("title"),
        "description": raw_data.get("description"),
        "channel_follower_count": raw_data.get("channel_follower_count"),
        "channel_follower_count_string": format_number(raw_data.get("channel_follower_count")),
        "channel_follower_count_compact_string": format_compact_number(raw_data.get("channel_follower_count")),
        "view_count": raw_data.get("view_count"),
        "view_count_string": format_number(raw_data.get("view_count")),
        "view_count_compact_string": format_compact_number(raw_data.get("view_count")),
        "banners": banners,
        "avatars": avatars,
    }

# Formats `/videos/{video_id}/formats` output
async def format_video_formats(raw_formats: List[Dict[str, Any]], filter_type: str = "all", duration: int = None) -> List[Dict[str, Any]]:
    formatted_formats = []
    for fmt in raw_formats:
        vcodec = fmt.get('vcodec')
        acodec = fmt.get('acodec')
        resolution = fmt.get('resolution')

        # Determine format type
        has_video = (vcodec != 'none' and vcodec is not None)
        is_audio_only = (vcodec == 'none' or vcodec is None) and (acodec != 'none' and acodec is not None)
        is_merged = (vcodec != 'none' and vcodec is not None) and (acodec != 'none' and acodec is not None)

        # Filter logic
        if filter_type == "video" and not has_video: continue
        if filter_type == "audio" and not is_audio_only: continue
        if filter_type == "merged" and not is_merged: continue

        filesize = fmt.get('filesize') or fmt.get('filesize_approx')
        if filesize is None and duration and fmt.get('tbr'):
            try:
                # Estimate filesize: (bitrate (kbit/s) * 1000 / 8) * duration (s)
                filesize = int((float(fmt['tbr']) * 1000 / 8) * float(duration))
            except (ValueError, TypeError):
                pass

        if resolution == 'audio only': pass
        elif not resolution and fmt.get('width') and fmt.get('height'): resolution = f"{fmt.get('width')}x{fmt.get('height')}"

        formatted_formats.append({
            'format_id': fmt.get('format_id'),
            'extension': fmt.get('ext'),
            'resolution': resolution,
            'filesize': filesize,
            'filesize_string': format_compact_number(filesize),
            'format_note': fmt.get('format_note'),
            'vcodec': vcodec,
            'acodec': acodec,
            'tbr': fmt.get('tbr')
        })
    return formatted_formats

async def format_download_filename(title: str, format_id: str, formats: List[Dict[str, Any]] = None) -> str:
    # Sanitize title
    safe_title = re.sub(r'[\\/*?:"<>|]', "", title)
    safe_title = safe_title.strip()
    
    # Fetch formats to find resolution/quality
    quality_label = ""
    extension = "mp4"
    
    if format_id != "b" and formats:
        for fmt in formats:
            if fmt.get("format_id") == format_id:
                resolution = fmt.get("resolution")
                note = fmt.get("format_note")
                ext = fmt.get("extension")

                if resolution and resolution != "audio only": quality_label = f"_{resolution}"
                elif note: quality_label = f"_{note}"
                if ext: extension = ext
                break
    else: quality_label = "_best"
    return f"{safe_title}{quality_label}.{extension}"
