# 📺 ShinTube API

This is a **FastAPI backend** that uses [`yt-dlp`](https://github.com/yt-dlp/yt-dlp) to fetch video metadata, search results, playlists, and downloadable formats from YouTube.

---

## 🚀 Features
- **Search YouTube videos** (`/search`)
- **Get video details & formats** (`/video/{id}`)
- **Fetch playlist metadata** (`/playlist/{id}`)
- **Download videos** in selected format (`/download/{id}`)
- **CORS enabled** for Flutter frontend
- **Clean modular structure** for scalability
- **Fast search results** with approximate upload dates
- **Multiple thumbnail resolutions**

---

## 📂 Project Structure

```
ShinTube-API/
├── main.py                    # FastAPI entrypoint
├── config.py                  # Settings, environment variables
├── routes/                    # API endpoints
│   ├── __init__.py
│   ├── search.py
│   ├── video.py
│   ├── playlist.py
│   └── download.py
├── services/                  # Business logic
│   ├── __init__.py
│   └── cache_service.py
│   └── ytdlp_service.py
├── utils/                     # Helpers & parsers
│   ├── format_parser.py
│   └── exceptions.py
└── README.md
```

---

## 📦 Installation

### 1. Prerequisites
- **Python 3.7+**
- **yt-dlp** installed globally or in your environment

### 2. Install yt-dlp
```bash
pip install yt-dlp
```

### 3. Clone and setup
```bash
git clone https://github.com/yourusername/ShinTube-API.git
cd ShinTube-API

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install fastapi uvicorn
```

---

## ▶️ Running the Server

```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at:
- **API**: http://localhost:8000
- **Swagger UI docs**: http://localhost:8000/docs
- **Health check**: http://localhost:8000

---

## 🌐 API Endpoints

| Method | Endpoint | Description | Params |
|--------|----------|-------------|--------|
| GET | `/` | Health check | - |
| GET | `/search` | Search YouTube videos | `q` (string), `limit` (int, 1-50) |
| GET | `/video/{video_id}` | Get video details & formats | - |
| GET | `/playlist/{playlist_id}` | Get playlist metadata & items | - |
| GET | `/download/{video_id}` | Download a video in selected format | `format` (string, optional) |

### Example Requests

**Search videos:**
```
GET /search?q=hello world
```

**Get video info:**
```
GET /video/dQw4w9WgXcQ
```

**Get playlist:**
```
GET /playlist/PLrAXtmRdnEQy_K7ZhqRZZTFPmcNfPfBTN
```

**Download video:**
```
GET /download/dQw4w9WgXcQ?format=best
```

---

## ⚙️ Environment Variables

Create a `.env` file in the root directory:

| Variable | Default Value | Description |
|----------|---------------|-------------|
| `API_NAME` | `"YouTube API Backend"` | Name of the API |
| `DEBUG` | `True` | Enable debug mode |
| `CACHE_EXPIRY_SECONDS` | `3600` | Cache lifetime in seconds |
| `ALLOWED_ORIGINS` | `["*"]` | Allowed CORS origins |

Example `.env` file:
```env
API_NAME=ShinTube API
DEBUG=False
CACHE_EXPIRY_SECONDS=7200
ALLOWED_ORIGINS=["http://localhost:3000", "https://yourdomain.com"]
```

---

## 📝 Response Format

**Search Response:**
```json
{
  "query": "hello world",
  "limit": 15,
  "results": [
    {
      "video_id": "u7JMhVI7taQ",
      "title": "Alan Walker & Torine - Hello World",
      "uploader": "Alan Walker",
      "duration": 176,
      "duration_string": "2:56",
      "view_count": 25503715,
      "view_count_string": "25.5M views",
      "upload_date": "20220815",
      "upload_date_string": "2 years ago",
      "thumbnails": [
        {
          "url": "https://img.youtube.com/vi/u7JMhVI7taQ/mqdefault.jpg",
          "width": 320,
          "height": 180,
          "resolution": "320x180"
        },
        {
          "url": "https://img.youtube.com/vi/u7JMhVI7taQ/hqdefault.jpg",
          "width": 480,
          "height": 360,
          "resolution": "480x360"
        }
      ],
      "url": "https://youtube.com/watch?v=u7JMhVI7taQ"
    }
  ]
}
```

---

## 📌 Notes

- This project does **not** bypass YouTube's Terms of Service — it only processes publicly available data.
- `yt-dlp` behavior can change if YouTube updates its site — keep `yt-dlp` updated.

---

## 🛠️ Development

To contribute or modify:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request