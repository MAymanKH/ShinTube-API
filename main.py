from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import search, video, playlist, download
from config import settings
from mangum import Mangum
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

# Mount routers
app.include_router(search.router, prefix="/search", tags=["search"])
app.include_router(video.router, prefix="/video", tags=["video"])
app.include_router(playlist.router, prefix="/playlist", tags=["playlist"])
app.include_router(download.router, prefix="/download", tags=["download"])

# Add handler for Vercel (serverless)
handler = Mangum(app)

if __name__ == "__main__":
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
    )
