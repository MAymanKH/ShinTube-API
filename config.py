from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Default values, can be changed in .env file
    API_NAME: str = "ShinTube API Backend"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    CACHE_EXPIRY_SECONDS: int = 3600
    RATE_LIMIT_ENABLED: bool = True
    DEFAULT_RATE_LIMIT: str = "100/minute"
    ALLOWED_ORIGINS: List[str] = ["*"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
