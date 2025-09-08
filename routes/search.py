from fastapi import APIRouter, Query, HTTPException
from services.ytdlp_service import search_videos
from utils import exceptions
from utils.logger import get_logger
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

router = APIRouter()
logger = get_logger(__name__)

@router.get("/")
async def search(
    q: str = Query(..., description="Search query"),
    limit: int = Query(15, ge=1, le=50, description="Number of results to return"),
    page: int = Query(1, ge=1, description="Page number"),
):

    try:
        logger.info(f"Searching for query: '{q}' with limit: {limit} and page: {page}")
        total_results_to_fetch = limit * page
        videos = await search_videos(q, total_results_to_fetch)
        start_index = limit * (page - 1)
        paged_results = videos[start_index : start_index + limit]
        logger.info(f"Found {len(paged_results)} results for query: '{q}'")
        return {"query": q, "limit": limit, "page": page, "results": paged_results}
    except exceptions.YTDLPError as e:
        logger.error(f"Search service failed for query: '{q}', error: {e}")
        raise HTTPException(status_code=500, detail=f"Search service failed: {str(e)}")
    except Exception as e:
        logger.error(f"An unexpected error occurred during search for query: '{q}', error: {e}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
