from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    API_NAME: str = "ShinTube API Backend"
    DEBUG: bool = True
    CACHE_EXPIRY_SECONDS: int = 3600
    ALLOWED_ORIGINS: List[str] = ["*"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
