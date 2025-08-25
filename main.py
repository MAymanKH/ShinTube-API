from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from routes import search, video, playlist, download
from config import settings
import uvicorn

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
app.include_router(video.router, prefix="/videos", tags=["videos"])
app.include_router(playlist.router, prefix="/playlists", tags=["playlists"])
app.include_router(download.router, prefix="/download", tags=["download"])

if __name__ == "__main__":
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
    )