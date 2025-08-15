from typing import Dict, List, Any
from datetime import datetime


def format_view_count(view_count: int) -> str:
    """Format view count into human-readable string"""
    if view_count is None:
        return "Unknown views"
    
    if view_count >= 1_000_000_000:
        return f"{view_count / 1_000_000_000:.1f}B views"
    elif view_count >= 1_000_000:
        return f"{view_count / 1_000_000:.1f}M views"
    elif view_count >= 1_000:
        return f"{view_count / 1_000:.1f}K views"
    else:
        return f"{view_count} views"


def format_relative_time(upload_date: str, release_year: int = None) -> str:
    """Format upload date into relative time string"""
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
        # Parse YYYYMMDD format
        upload_dt = datetime.strptime(upload_date, "%Y%m%d")
        now = datetime.now()
        diff = now - upload_dt
        
        days = diff.days
        if days < 0: return "In the future" # Should not happen
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


def format_duration(duration) -> str:
    """Format duration in seconds to human-readable string"""
    if duration is None:
        return "Unknown"
    
    # Convert to int if it's a float
    try:
        duration = int(duration)
    except (ValueError, TypeError):
        return "Unknown"
    
    hours = duration // 3600
    minutes = (duration % 3600) // 60
    seconds = duration % 60
    
    if hours > 0:
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes}:{seconds:02d}"


def format_video_info(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format yt-dlp raw JSON output into a clean structure
    
    Args:
        raw_data: Raw JSON data from yt-dlp
        
    Returns:
        Cleaned and formatted video information dictionary
    """
    # Extract thumbnails
    thumbnails = []
    if raw_data.get('thumbnails'):
        for thumb in raw_data['thumbnails']:
            if thumb.get('url'):
                thumbnails.append({
                    'url': thumb['url'],
                    'width': thumb.get('width'),
                    'height': thumb.get('height'),
                    'id': thumb.get('id')
                })
    
    # Extract formats
    formats = []
    if raw_data.get('formats'):
        for fmt in raw_data['formats']:
            formats.append({
                'id': fmt.get('format_id'),
                'resolution': fmt.get('resolution') or f"{fmt.get('width', 'unknown')}x{fmt.get('height', 'unknown')}",
                'ext': fmt.get('ext'),
                'filesize': fmt.get('filesize'),
                'vcodec': fmt.get('vcodec'),
                'acodec': fmt.get('acodec'),
                'fps': fmt.get('fps'),
                'tbr': fmt.get('tbr')
            })
    
    return {
        'video_id': raw_data.get('id'),
        'title': raw_data.get('title'),
        'description': raw_data.get('description'),
        'uploader': raw_data.get('uploader') or raw_data.get('channel'),
        'duration': raw_data.get('duration'),
        'view_count': raw_data.get('view_count'),
        'upload_date': raw_data.get('upload_date'),
        'thumbnails': thumbnails,
        'formats': formats,
        'webpage_url': raw_data.get('webpage_url'),
        'original_url': raw_data.get('original_url')
    }


def format_playlist_info(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format yt-dlp raw playlist JSON output into a clean structure
    
    Args:
        raw_data: Raw JSON data from yt-dlp for playlist
        
    Returns:
        Cleaned and formatted playlist information dictionary
    """
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


def format_search_results(raw_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Format yt-dlp search results into a clean structure
    
    Args:
        raw_results: List of raw JSON search results from yt-dlp
        
    Returns:
        List of cleaned and formatted video information dictionaries
    """
    formatted_results = []
    for result in raw_results:
        # Use upload_date directly from yt-dlp output
        upload_date = result.get('upload_date')
        
        view_count = result.get('view_count')
        duration = result.get('duration')
        
        # Generate thumbnail URLs from video ID - only two resolutions
        video_id = result.get('id')
        thumbnails = []
        if video_id:
            # YouTube thumbnail URL patterns - only medium and high quality
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
        
        # Use existing thumbnails if available, otherwise use generated ones
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
            # Limit to only 2 thumbnails
            if existing_thumbnails:
                thumbnails = existing_thumbnails[:2]
        
        formatted_results.append({
            'video_id': video_id,
            'title': result.get('title'),
            'uploader': result.get('uploader') or result.get('channel') or result.get('channel_id'),
            'duration': duration,
            'duration_string': format_duration(duration),
            'view_count': view_count,
            'view_count_string': format_view_count(view_count) if view_count else "Unknown views",
            'upload_date': upload_date,
            'upload_date_string': format_relative_time(upload_date) if upload_date else "Unknown",
            'thumbnails': thumbnails,
            'url': result.get('url') or f"https://youtube.com/watch?v={video_id}" if video_id else None
        })
    
    return formatted_results