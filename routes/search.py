from fastapi import APIRouter, Query, HTTPException
from typing import Optional
import sys
import os

# Add parent directory to path to import services
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


router = APIRouter()


@router.get("/")
async def search(
    q: Optional[str] = Query(None, description="Search query"),
    page: int = Query(1, ge=1, description="Page number (1-based)"),
    limit: int = Query(20, gt=0, description="Number of results per page"),
):
    """
    Search YouTube videos with pagination and caching support.
    
    - **q**: Search query string (required)
    - **page**: Page number starting from 1 (default: 1)
    - **limit**: Number of results per page (default: 20)
    
    Returns paginated results with metadata including has_more indicator.
    Results are cached for a few minutes to support efficient pagination.
    """
    if not q:
        raise HTTPException(status_code=422, detail="Query parameter 'q' is required")
    
    # Validate pagination parameters
    if page < 1:
        raise HTTPException(status_code=400, detail="Page must be >= 1")
    
    if limit <= 0:
        raise HTTPException(status_code=400, detail="Limit must be > 0")

    try:
        from services import ytdlp_service
        from services.search_cache import search_cache
        
        # Check cache first
        cached_results = search_cache.get(q)
        
        if cached_results is None:
            # Cache miss - fetch results from YouTube with a reasonable limit for caching
            # Fetch up to 100 results to support multiple pages
            cache_limit = min(100, max(50, limit * 5))  # Fetch enough for several pages
            
            cached_results = await ytdlp_service.search_videos(q, cache_limit)
            search_cache.set(q, cached_results)
        
        # Calculate pagination
        start_index = (page - 1) * limit
        end_index = start_index + limit
        
        # Get the slice of results for this page
        paginated_results = cached_results[start_index:end_index]
        
        # Determine if there are more results
        has_more = end_index < len(cached_results)
        
        return {
            "query": q,
            "page": page,
            "limit": limit,
            "has_more": has_more,
            "results": paginated_results
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")
