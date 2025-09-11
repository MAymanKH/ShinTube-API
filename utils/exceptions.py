class YTDLPError(Exception):
    """Base exception for errors raised by the ytdlp_service."""
    pass

class VideoNotFoundError(YTDLPError):
    """Raised when a video cannot be found or is unavailable."""
    pass

class PlaylistNotFoundError(YTDLPError):
    """Raised when a playlist cannot be found or is unavailable."""
    pass

class ChannelNotFoundError(YTDLPError):
    """Raised when a channel cannot be found or is unavailable."""
    pass

class DataParsingError(YTDLPError):
    """Raised when formatting or parsing of successfully fetched data fails."""
    pass
