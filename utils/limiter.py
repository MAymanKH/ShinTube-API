from slowapi import Limiter
from slowapi.util import get_remote_address
from config import settings

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[
        settings.RATE_LIMIT_PER_SECOND,
        settings.RATE_LIMIT_PER_MINUTE,
        settings.RATE_LIMIT_PER_HOUR
    ] if settings.RATE_LIMIT_ENABLED else [],
    enabled=settings.RATE_LIMIT_ENABLED
)
