from cachetools import TTLCache
from functools import wraps
from config import settings
from utils.logger import logger

# Initialize cache with settings
# Maxsize 1000 items, TTL from settings
cache = TTLCache(maxsize=1000, ttl=settings.CACHE_EXPIRY_SECONDS)

def cached(key_builder=None):
    """
    A decorator to cache the result of an async function.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if key_builder:key = key_builder(*args, **kwargs) # Generate key
            else:key = f"{func.__name__}:{str(args)}:{str(kwargs)}" # Simple key generation based on function name and arguments
            
            # Check cache
            if key in cache:
                logger.debug(f"Cache hit for key: {key}")
                return cache[key]
            
            # Execute function
            logger.debug(f"Cache miss for key: {key}")
            result = await func(*args, **kwargs)
            
            # Store in cache
            cache[key] = result
            return result
        return wrapper
    return decorator
