class YTDLPError(Exception):
    """Base exception for errors raised by the ytdlp_service."""
    pass

class VideoNotFoundError(YTDLPError):
    """Raised when a video cannot be found or is unavailable."""
    pass

class PlaylistNotFoundError(YTDLPError):
    """Raised when a playlist cannot be found or is unavailable."""
    pass

class DownloadError(YTDLPError):
    """Raised when a video download fails."""
    pass