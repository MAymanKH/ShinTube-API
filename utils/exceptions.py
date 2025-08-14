class VideoNotFoundException(Exception):
    """Exception raised when a video is not found"""
    
    def __init__(self, message: str = "Video not found"):
        self.message = message
        super().__init__(self.message)


class PlaylistNotFoundException(Exception):
    """Exception raised when a playlist is not found"""
    
    def __init__(self, message: str = "Playlist not found"):
        self.message = message
        super().__init__(self.message)


class DownloadFailedException(Exception):
    """Exception raised when video download fails"""
    
    def __init__(self, message: str = "Download failed"):
        self.message = message
        super().__init__(self.message)
