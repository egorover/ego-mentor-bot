"""Logging configuration module."""

import sys

from loguru import logger

from src.infrastructure.config.settings import settings


def setup_logging() -> None:
    """Configure logging for the application."""

    # Remove default handler
    logger.remove()

    # Add console handler
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
        level=settings.log_level,
        colorize=True,
    )

    # Add file handler for errors
    logger.add(
        "logs/error.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function} - {message}",
        level="ERROR",
        rotation="1 week",
        retention="1 month",
    )

    # Add file handler for all logs
    logger.add(
        "logs/app.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function} - {message}",
        level="DEBUG",
        rotation="1 day",
        retention="7 days",
    )

    logger.info(f"Logging configured. Environment: {settings.environment}")


# Setup on import
setup_logging()
