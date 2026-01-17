<div align="center">
<img src = "https://mohamedayman.net/assets/icons/st_icon_big.png" width = 200>

# ShinTube API

A FastAPI backend that acts as a [`yt-dlp`](https://github.com/yt-dlp/yt-dlp) wrapper to provide a RESTful API for downloading and fetching public data from YouTube.

</div>

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [1. Using Docker (Recommended)](#1-using-docker-recommended)
  - [2. Local Python Environment](#2-local-python-environment)
- [Environment Variables](#environment-variables)
- [API Endpoints](#api-endpoints)
  - [Example Requests & Responses](#example-requests-&-responses)
- [Notes](#notes)
- [Contributing](#contributing)

---

## Features

-   **Search YouTube videos and playlists** with optional limits and pagination.
-   **Get comprehensive video details** including metrics, thumbnails, etc.
-   **Get video formats and download videos** directly as a stream.
-   **Fetch video comments** with replies and commenters metadata.
-   **Retrieve available video subtitles** in any format or language.
-   **Fetch playlist metadata** and all its videos.
-   **Get comprehensive channel details**.
-   **Fetch a channel's videos** with an optional limit.
-   **In-memory Caching** for improved performance on repeated requests.
-   **Rate Limiting** to prevent abuse and ensure stability.
-   **Built with FastAPI** for high performance.
-   **Asynchronous support** for non-blocking requests.
-   **Easily configurable** via environment variables.
-   **Clean, modular, and scalable** project structure.
-   **Containerized** with Docker for easy setup and deployment.

---

## Project Structure

```
ShinTube-API/
├── .dockerignore
├── .gitignore
├── config.py                  # Settings and environment variables
├── docker-compose.yml         # Docker Compose configuration
├── Dockerfile                 # Docker configuration
├── main.py                    # FastAPI application entrypoint
├── README.md
├── requirements.txt           # Python dependencies
├── logs/                      # Log files
├── routes/                    # API endpoints (routers)
│   ├── __init__.py
│   ├── channels.py
│   ├── playlists.py
│   ├── search.py
│   └── videos.py
├── services/                  # Business logic
│   ├── __init__.py
│   ├── cache_service.py
│   └── ytdlp_service.py
└── utils/                     # Helper functions and utilities
    ├── __init__.py
    ├── exceptions.py
    ├── format_parser.py
    ├── limiter.py
    └── logger.py
```

---

## Getting Started

You can run the project using Docker (recommended) or by setting up a local Python environment.

### 1. Using Docker (Recommended)

**Prerequisites:**
*   **Docker** and **Docker Compose** installed.

**Instructions:**
1.  Clone the repository:
    ```bash
    git clone https://github.com/MAymanKH/ShinTube-API.git
    cd ShinTube-API
    ```
2.  Build and run the container using Docker Compose:
    ```bash
    docker-compose up --build
    ```
The API will be running and accessible at `http://localhost:8000`.

### 2. Local Python Environment

**Prerequisites:**
*   **Python 3.8+** installed and available in your system's PATH.

**Instructions:**
1.  Clone the repository:
    ```bash
    git clone https://github.com/MAymanKH/ShinTube-API.git
    cd ShinTube-API
    ```
2.  Create and activate a virtual environment: (Optional)
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  Install the required Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Run the API:
    ```bash
    python main.py
    ```

---

## Environment Variables

The application can be configured using environment variables. You can create a `.env` file in the root directory to manage them.

| Variable          | Default Value | Description                               |
| :---------------- | :------------ | :---------------------------------------- |
| `API_NAME`        | `ShinTube API`| The name of the API.                      |
| `HOST`            | `0.0.0.0`     | The host address for the server.          |
| `PORT`            | `8000`        | The port for the server.                  |
| `DEBUG`           | `True`        | Toggles debug mode.                       |
| `CACHE_EXPIRY_SECONDS` | `3600`   | Cache TTL in seconds.                     |
| `RATE_LIMIT_ENABLED` | `True`     | Enable or disable rate limiting.          |
| `RATE_LIMIT_PER_SECOND` | `5` | Rate limit per second per IP.          |
| `RATE_LIMIT_PER_MINUTE` | `100` | Rate limit per minute per IP.          |
| `RATE_LIMIT_PER_HOUR` | `1000` | Rate limit per hour per IP.             |
| `ALLOWED_ORIGINS` | `["*"]`       | A list of allowed CORS origins.           |

**Example `.env` file:**
```env
API_NAME="My ShinTube API"
HOST="0.0.0.0"
PORT=8000
DEBUG=False
CACHE_EXPIRY_SECONDS=1800
RATE_LIMIT_ENABLED=True
RATE_LIMIT_PER_SECOND=2
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=500
ALLOWED_ORIGINS='["http://localhost:8000", "https://my-frontend.com"]'
```

---

## API Endpoints

The API documentation is automatically generated by Swagger UI and is available at `http://localhost:8000/docs`.

| Method | Endpoint                      | Description                               | Arguments |
| :----- | :---------------------------- | :---------------------------------------- | :-------- |
| GET    | `/`                           | Health check for the API.                 | None |
| GET    | `/docs`                       | Full API documentation.                   | None |
| GET    | `/search`                     | Search for YouTube videos.                | `q` (str), `type` (str, default="video"), `limit` (int, default=15), `page` (int, default=1), `enrich` (bool, default=True) |
| GET    | `/videos/{video_id}`          | Get details for a specific video.         | None |
| GET    | `/videos/{video_id}/comments` | Get comments for a specific video.        | None |
| GET    | `/videos/{video_id}/subtitles`| Get subtitles for a specific video.       | None |
| GET    | `/videos/{video_id}/formats`  | Get available formats for a video.        | `type` (str, default="all") |
| GET    | `/videos/{video_id}/download` | Stream a specific video format.           | `format_id` (str, default="b") |
| GET    | `/playlists/{playlist_id}`    | Get metadata and videos for a playlist.   | None |
| GET    | `/channels/{channel_id}`      | Get details for a specific channel.       | None |
| GET    | `/channels/{channel_id}/videos`| Get videos for a specific channel.        | `limit` (int, default=100) |

<a id="example-requests-&-responses"></a>
### Example Requests & Responses

<details>
<summary><b>Search for videos</b></summary>

Request:
`GET /search?q=fastapi&limit=5&page=1`

Response:
```json
{
  "query": "fastapi",
  "type": "video",
  "limit": 5,
  "page": 1,
  "results": [
    {
      "video_id": "58Tn2xB8kIE",
      "url": "https://www.youtube.com/watch?v=58Tn2xB8kIE",
      "title": "The Most Important Skills Going Forward with CTO + Homebrew Maintainer Mike McQuaid [Podcast #204]",
      "live_status": null,
      "uploader": null,
      "duration": 5262.0,
      "duration_string": "1:27:42",
      "view_count": 7249,
      "view_count_string": "7.2K",
      "upload_date": "20260117",
      "upload_date_string": "Today",
      "thumbnails": [
        {
          "url": "https://img.youtube.com/vi/58Tn2xB8kIE/mqdefault.jpg",
          "width": 320,
          "height": 180,
          "resolution": "320x180"
        }
      ]
    },
    {
      "video_id": "tLKKmouUams",
      "url": "https://www.youtube.com/watch?v=tLKKmouUams",
      "title": "FastAPI Course for Beginners",
      "live_status": null,
      "uploader": null,
      "duration": 3873.0,
      "duration_string": "1:04:33",
      "view_count": 493090,
      "view_count_string": "493.1K",
      "upload_date": "20210812",
      "upload_date_string": "Aug 12, 2021",
      "thumbnails": [
        {
          "url": "https://img.youtube.com/vi/tLKKmouUams/mqdefault.jpg",
          "width": 320,
          "height": 180,
          "resolution": "320x180"
        }
      ]
    },
    {
      "video_id": "0sOvCWFmrtA",
      "url": "https://www.youtube.com/watch?v=0sOvCWFmrtA",
      "title": "Python FastAPI Tutorial: Build a REST API in 15 Minutes",
      "live_status": null,
      "uploader": null,
      "duration": 912.0,
      "duration_string": "15:12",
      "view_count": 389057,
      "view_count_string": "389.1K",
      "upload_date": "20201103",
      "upload_date_string": "Nov 3, 2020",
      "thumbnails": [
        {
          "url": "https://img.youtube.com/vi/0sOvCWFmrtA/mqdefault.jpg",
          "width": 320,
          "height": 180,
          "resolution": "320x180"
        }
      ]
    },
    {
      "video_id": "gQTRsZPi7qa",
      "url": "https://www.youtube.com/watch?v=gQTRsZPi7qa",
      "title": "FastAPI - A Python Web Framework",
      "live_status": null,
      "uploader": null,
      "duration": 605.0,
      "duration_string": "10:05",
      "view_count": 69022,
      "view_count_string": "69.0K",
      "upload_date": "20191208",
      "upload_date_string": "Dec 8, 2019",
      "thumbnails": [
        {
          "url": "https://img.youtube.com/vi/gQTRsZPi7qa/mqdefault.jpg",
          "width": 320,
          "height": 180,
          "resolution": "320x180"
        }
      ]
    },
    {
      "video_id": "3A7TJ9V1Y54",
      "url": "https://www.youtube.com/watch?v=3A7TJ9V1Y54",
      "title": "FastAPI Full Course - Learn FastAPI in 2023",
      "live_status": null,
      "uploader": null,
      "duration": 14035.0,
      "duration_string": "3:53:55",
      "view_count": 14619,
      "view_count_string": "14.6K",
      "upload_date": "20230225",
      "upload_date_string": "Feb 25, 2023",
      "thumbnails": [
        {
          "url": "https://img.youtube.com/vi/3A7TJ9V1Y54/mqdefault.jpg",
          "width": 320,
          "height": 180,
          "resolution": "320x180"
        }
      ]
    }
  ]
}
```
</details>

<details>
<summary><b>Get video information</b></summary>

Request:
`GET /videos/tLKKmouUams`

Response:
```json
{
  "video_id": "tLKKmouUams",
  "url": "https://www.youtube.com/watch?v=tLKKmouUams",
  "title": "FastAPI Course for Beginners",
  "description": "This video is a full FastAPI crash course. In the course, you will learn everything you need to know to start building APIs using FastAPI.\n\n✏️ Course developed by Code With Tomi. Check out his channel: https://www.youtube.com/c/CodeWithTomi\n\n🔗 Download a free FastAPI Cheat Sheet - https://codewithtomi.eo.page/nnr3t\n\n🔗 Join Code With Tomi's Discord Server - https://discord.gg/cjqNBHHhKV\n🔗 Twitter: https://twitter.com/TomiTokko3\n\n⭐️ Course Contents ⭐️\n⌨️ (0:00:00) Intro     \n⌨️ (0:01:10) Installation and Creating Your First API\n⌨️ (0:15:35) Path Parameters\n⌨️ (0:27:24) Query Parameters\n⌨️ (0:37:36) Combining Path and Query Parameters\n⌨️ (0:39:50) Request Body and The Post Method\n⌨️ (0:46:58) Put Method \n⌨️ (1:00:26) Delete Method  \n\n🎉 Thanks to our Champion and Sponsor supporters:\n👾 Wong Voon jinq\n👾 hexploitation\n👾 Katia Moran\n👾 BlckPhantom\n👾 Nick Raker\n👾 Otis Morgan\n👾 DeezMaster\n👾 Treehouse\n👾 AppWrite\n\n--\n\nLearn to code for free and get a developer job: https://www.freecodecamp.org\n\nRead hundreds of articles on programming: https://freecodecamp.org/news \n\n❤️ Support for this channel comes from our friends at Scrimba – the coding platform that's reinvented interactive learning: https://scrimba.com/freecodecamp",
  "channel": "freeCodeCamp.org",
  "channel_id": "UC8butISFwT-Wl7EV0hUK0BQ",
  "channel_url": "https://www.youtube.com/channel/UC8butISFwT-Wl7EV0hUK0BQ",
  "channel_follower_count": 11400000,
  "channel_follower_count_string": "11,400,000",
  "channel_follower_count_compact_string": "11.4M",
  "uploader": "freeCodeCamp.org",
  "duration": 3873,
  "duration_string": "1:04:33",
  "view_count": 493090,
  "view_count_string": "493,090",
  "view_count_compact_string": "493.1K",
  "like_count": 8797,
  "like_count_string": "8,797",
  "like_count_compact_string": "8.8K",
  "publish_date": "20210812",
  "publish_date_string": "Aug 12, 2021",
  "relative_publish_date": "4 years ago",
  "thumbnails": [
    {
      "url": "https://img.youtube.com/vi/tLKKmouUams/mqdefault.jpg",
      "width": 320,
      "height": 180,
      "resolution": "320x180"
    },
    {
      "url": "https://img.youtube.com/vi/tLKKmouUams/hqdefault.jpg",
      "width": 480,
      "height": 360,
      "resolution": "480x360"
    },
    {
      "url": "https://img.youtube.com/vi/tLKKmouUams/maxresdefault.jpg",
      "width": 1280,
      "height": 720,
      "resolution": "1280x720"
    }
  ]
}
```
</details>

<details>
<summary><b>Get video comments</b></summary>

Request:
`GET /videos/tLKKmouUams/comments`

Response:
```json
{
  "video_id": "tLKKmouUams",
  "result": {
    "comment_count": 50,
    "comments": [
      {
        "comment_id": "UgyERC4nojmhct1yFfx4AaABAg",
        "text": "The import path section doesn't work anymore with the None default. On line 18, leave out \"NONE\". def student(student_id: int = Path(description=\"input the Id of the student\"))",
        "author": "@akhatgrant133",
        "author_id": "UCB1KHcP17tjxR1VZYxkShaA",
        "author_url": "https://www.youtube.com/channel/UCB1KHcP17tjxR1VZYxkShaA",
        "like_count": 166,
        "like_count_string": "166",
        "is_hearted": false,
        "is_pinned": false,
        "timestamp": 1705536000,
        "time_text": "2 years ago",
        "reply_count": 0,
        "replies": []
      },
      {
        "comment_id": "Ugw9PkbgRg7KkNnwcrB4AaABAg",
        "text": ">get out of shower\n>need to learn fastapi\n>this\ni swear to god i'm being watched.",
        "author": "@heiscalledinvinciblenotinv68",
        "author_id": "UCrRGM_vSXO8jj4YECHQBKRA",
        "author_url": "https://www.youtube.com/channel/UCrRGM_vSXO8jj4YECHQBKRA",
        "like_count": 83,
        "like_count_string": "83",
        "is_hearted": false,
        "is_pinned": false,
        "timestamp": 1642464000,
        "time_text": "4 years ago",
        "reply_count": 0,
        "replies": []
      }
    ]
  }
}
```
</details>

<details>
<summary><b>Get video subtitles</b></summary>

Request:
`GET /videos/tLKKmouUams/subtitles`

Response:
```json
{
  "video_id": "tLKKmouUams",
  "subtitles": [
    {
      "language_code": "en",
      "language_name": "English",
      "is_auto_generated": false,
      "is_auto_translated": false,
      "formats": [
        {
          "ext": "json3",
          "url": "https://www.youtube.com/api/timedtext?v=tLKKmouUams..."
        },
        {
          "ext": "srv1",
          "url": "https://www.youtube.com/api/timedtext?v=tLKKmouUams..."
        },
        {
          "ext": "vtt",
          "url": "https://www.youtube.com/api/timedtext?v=tLKKmouUams..."
        }
      ]
    }
  ]
}
```
</details>

<details>
<summary><b>Get video formats</b></summary>

Request:
`GET /videos/tLKKmouUams/formats?type=merged`

Response:
```json
{
  "video_id": "tLKKmouUams",
  "formats": [
    {
      "format_id": "18",
      "extension": "mp4",
      "resolution": "640x358",
      "filesize": 76617552,
      "filesize_string": "76.6M",
      "format_note": "360p",
      "vcodec": "avc1.42001E",
      "acodec": "mp4a.40.2",
      "tbr": 158.261
    },
    {
      "format_id": "96",
      "extension": "mp4",
      "resolution": "1920x1072",
      "filesize": null,
      "filesize_string": null,
      "format_note": null,
      "vcodec": "avc1.640028",
      "acodec": "mp4a.40.2",
      "tbr": 1374.122
    }
  ]
}
```
</details>

<details>
<summary><b>Download video</b></summary>

Request:
`GET /videos/tLKKmouUams/download?format_id=18`

Response:
```
starts file streaming
```
</details>

<details>
<summary><b>Get playlist information</b></summary>

Request:
`GET /playlists/PLsyeobzWxl7qF4ASwCZZDXor_Y0YJ3Qfc`

Response:
```json
{
  "playlist_id": "PLsyeobzWxl7qF4ASwCZZDXor_Y0YJ3Qfc",
  "title": "FastAPI Tutorial | Python Web Framework",
  "description": null,
  "uploader": "Telusko",
  "channel_id": "@Telusko",
  "channel_url": "https://www.youtube.com/@Telusko",
  "item_count": 13,
  "videos": [
    {
      "video_id": "02dzgC_Ba70",
      "url": "https://www.youtube.com/watch?v=02dzgC_Ba70",
      "title": "#1 FastAPI - Python Web Framework",
      "live_status": null,
      "uploader": null,
      "duration": 415,
      "duration_string": "6:55",
      "view_count": 59000,
      "view_count_string": "59.0K",
      "upload_date": null,
      "upload_date_string": "Unknown",
      "thumbnails": [
        {
          "url": "https://img.youtube.com/vi/02dzgC_Ba70/mqdefault.jpg",
          "width": 320,
          "height": 180,
          "resolution": "320x180"
        }
      ]
    }
  ],
  "webpage_url": "https://www.youtube.com/playlist?list=PLsyeobzWxl7qF4ASwCZZDXor_Y0YJ3Qfc"
}
```
</details>

<details>
<summary><b>Get channel information</b></summary>

Request:
`GET /channels/UC8butISFwT-Wl7EV0hUK0BQ`

Response:
```json
{
  "channel_id": "UC8butISFwT-Wl7EV0hUK0BQ",
  "channel_url": "https://www.youtube.com/channel/UC8butISFwT-Wl7EV0hUK0BQ",
  "title": "freeCodeCamp.org",
  "description": "Learn math, programming, and computer science for free. A 501(c)(3) tax-exempt charity. We also run a free learning interactive platform at freecodecamp.org",
  "channel_follower_count": 11400000,
  "channel_follower_count_string": "11,400,000",
  "channel_follower_count_compact_string": "11.4M",
  "view_count": null,
  "view_count_string": null,
  "view_count_compact_string": null,
  "banners": [
    {
      "url": "https://yt3.googleusercontent.com/...",
      "height": 175,
      "width": 1060,
      "preference": -10,
      "id": "0",
      "resolution": "1060x175"
    }
  ],
  "avatars": [
    {
      "url": "https://yt3.googleusercontent.com/...",
      "height": 900,
      "width": 900,
      "id": "7",
      "resolution": "900x900"
    }
  ]
}
```
</details>

<details>
<summary><b>Get channel videos</b></summary>

Request:
`GET /channels/UC8butISFwT-Wl7EV0hUK0BQ/videos?limit=10`

Response:
```json
{
  "channel_id": "UC8butISFwT-Wl7EV0hUK0BQ",
  "videos": [
    {
      "video_id": "58Tn2xB8kIE",
      "url": "https://www.youtube.com/watch?v=58Tn2xB8kIE",
      "title": "The Most Important Skills Going Forward with CTO + Homebrew Maintainer Mike McQuaid [Podcast #204]",
      "live_status": null,
      "uploader": null,
      "duration": 5262.0,
      "duration_string": "1:27:42",
      "view_count": 7249,
      "view_count_string": "7.2K",
      "upload_date": "20260117",
      "upload_date_string": "Today",
      "thumbnails": [
        {
          "url": "https://img.youtube.com/vi/58Tn2xB8kIE/mqdefault.jpg",
          "width": 320,
          "height": 180,
          "resolution": "320x180"
        }
      ]
    }
  ]
}
```
</details>

---

## Notes

*   This project acts as a wrapper around the `yt-dlp` command-line tool. Its functionality is dependent on `yt-dlp`.
*   YouTube's structure can change, which may break `yt-dlp`. Keep `yt-dlp` updated to ensure the API remains functional.
*   This project does not bypass any of YouTube's Terms of Service; it only retrieves publicly available data.
*   This project is distributed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for more details.

---

## Contributing

Contributions are welcome! To contribute:

1.  Fork the repository.
2.  Create a new feature branch (`git checkout -b feature/YourFeature`).
3.  Make your changes and commit them (`git commit -m 'Add some feature'`).
4.  Push to the branch (`git push origin feature/YourFeature`).
5.  Open a Pull Request.
