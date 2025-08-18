from fastapi import APIRouter, Query, HTTPException
from services import ytdlp_service
from typing import Optional
import sys
import os

# Add parent directory to path to import services
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

router = APIRouter()

@router.get("/")
async def search(
    q: Optional[str] = Query(None, description="Search query"),
    limit: int = Query(15, ge=1, le=50, description="Number of results to return"),
    page: int = Query(1, ge=1, description="Page number"),
):
    if not q:
        raise HTTPException(status_code=422, detail="Query parameter 'q' is required")

    try:
        total_results = limit * page
        videos = await ytdlp_service.search_videos(q, total_results)
        start = limit * (page - 1)
        end = start + limit
        paged_results = videos[start:end] if start < len(videos) else []
        return {"query": q, "limit": limit, "page": page, "results": paged_results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")
