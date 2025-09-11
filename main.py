from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from routes import search, videos, playlists, channels
from config import settings
from utils.logger import logger
import uvicorn
import time

app = FastAPI(
    title=settings.API_NAME,
    version="1.0.0",
    debug=settings.DEBUG
)

# Enable CORS using config settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.info(f"request_method={request.method} request_path={request.url.path} status_code={response.status_code} process_time={formatted_process_time}ms")
    return response

# Health check endpoint
@app.get("/")
async def health_check():
    return {
        "status": "ok",
        "api_name": settings.API_NAME,
        "debug": settings.DEBUG
    }

# Dismissing favicon 404 errors
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204) # 204 No Content

# Mount routers
app.include_router(search.router, prefix="/search", tags=["search"])
app.include_router(videos.router, prefix="/videos", tags=["videos"])
app.include_router(playlists.router, prefix="/playlists", tags=["playlists"])
app.include_router(channels.router, prefix="/channels", tags=["channels"])

if __name__ == "__main__":
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
    )
