import time
from typing import List, Dict, Any, Optional
import sys
import os

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import settings


class SearchCache:
    """Simple in-memory cache for search results with expiration"""
    
    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}
    
    def get(self, query: str) -> Optional[List[Dict[str, Any]]]:
        """
        Get cached search results for a query
        
        Args:
            query: Search query string
            
        Returns:
            List of search results if cached and not expired, None otherwise
        """
        if query not in self._cache:
            return None
        
        cache_entry = self._cache[query]
        
        # Check if cache entry has expired
        if time.time() - cache_entry["timestamp"] > settings.CACHE_EXPIRY_SECONDS:
            # Remove expired entry
            del self._cache[query]
            return None
        
        return cache_entry["results"]
    
    def set(self, query: str, results: List[Dict[str, Any]]) -> None:
        """
        Cache search results for a query
        
        Args:
            query: Search query string
            results: List of search results to cache
        """
        self._cache[query] = {
            "results": results,
            "timestamp": time.time()
        }
    
    def clear_expired(self) -> None:
        """Remove all expired cache entries"""
        current_time = time.time()
        expired_keys = [
            key for key, value in self._cache.items()
            if current_time - value["timestamp"] > settings.CACHE_EXPIRY_SECONDS
        ]
        
        for key in expired_keys:
            del self._cache[key]
    
    def clear_all(self) -> None:
        """Clear all cache entries"""
        self._cache.clear()
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        current_time = time.time()
        active_entries = sum(
            1 for value in self._cache.values()
            if current_time - value["timestamp"] <= settings.CACHE_EXPIRY_SECONDS
        )
        
        return {
            "total_entries": len(self._cache),
            "active_entries": active_entries,
            "expired_entries": len(self._cache) - active_entries
        }


# Global cache instance
search_cache = SearchCache()