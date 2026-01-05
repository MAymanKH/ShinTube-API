from fastapi import APIRouter, Query, HTTPException, Request
from services.ytdlp_service import search_videos, search_playlists
from utils import exceptions
from utils.logger import logger
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

router = APIRouter()

@router.get("/")
async def search(
    request: Request,
    q: str = Query(..., description="Search query"),
    type: str = Query("video", enum=["video", "playlist"], description="Type of content to search for"),
    limit: int = Query(15, ge=1, le=50, description="Number of results to return"),
    page: int = Query(1, ge=1, description="Page number"),
    enrich: bool = Query(True, description="Enrich playlist metadata (slower)"),
):

    try:
        logger.info(f"Searching for query: '{q}' with type: '{type}', limit: {limit} and page: {page}")
        total_results_to_fetch = limit * page

        if type == "playlist": results = await search_playlists(q, total_results_to_fetch, enrich_metadata=enrich)
        else:results = await search_videos(q, total_results_to_fetch)

        start_index = limit * (page - 1)
        paged_results = results[start_index : start_index + limit]
        logger.info(f"Found {len(results)} results for query: '{q}' (returning {len(paged_results)})")
        return {"query": q, "type": type, "limit": limit, "page": page, "results": paged_results}
    except exceptions.YTDLPError as e:
        logger.error(f"Search service failed for query: '{q}', error: {e}")
        raise HTTPException(status_code=500, detail=f"Search service failed: {str(e)}")
    except Exception as e:
        logger.error(f"An unexpected error occurred during search for query: '{q}', error: {e}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
