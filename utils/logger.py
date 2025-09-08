import sys
import os
from loguru import logger
from config import settings

LOG_FORMAT = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> - <level>{level: <8}</level> - <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"

if not os.path.exists("logs"):
    os.makedirs("logs")

# Remove default handler
logger.remove()

# Console logger
logger.add(
    sys.stdout,
    colorize=True,
    format=LOG_FORMAT,
    level="DEBUG" if settings.DEBUG else "INFO",
)

# File logger
logger.add(
    "logs/app.log",
    rotation="00:00",
    retention="7 days",
    encoding="utf-8",
    level="INFO",
    format=LOG_FORMAT,
    enqueue=True,  # Make logging asynchronous
    backtrace=True,
    diagnose=settings.DEBUG,
)

__all__ = ["logger"]
