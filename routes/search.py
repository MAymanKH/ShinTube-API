from fastapi import APIRouter, Query, HTTPException
from services.ytdlp_service import search_videos
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

router = APIRouter()

@router.get("/")
async def search(
    q: str = Query(..., description="Search query"),
    limit: int = Query(15, ge=1, le=50, description="Number of results to return"),
    page: int = Query(1, ge=1, description="Page number"),
):

    try:
        total_results = limit * page
        videos = await search_videos(q, total_results)
        start = limit * (page - 1)
        end = start + limit
        paged_results = videos[start:end] if start < len(videos) else []
        return {"query": q, "limit": limit, "page": page, "results": paged_results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")
