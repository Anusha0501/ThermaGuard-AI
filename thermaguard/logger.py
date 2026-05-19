"""
Centralized logging configuration using Loguru.

Provides structured logging with rotation, compression, and multiple sinks.
"""

import sys
from loguru import logger
from thermaguard.config import settings


def setup_logger() -> None:
    """Configure Loguru logger with appropriate sinks based on environment."""
    
    # Remove default handler
    logger.remove()
    
    # Console output with color
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=settings.log_level,
        colorize=True,
    )
    
    # File output with rotation
    logger.add(
        "logs/thermaguard_{time:YYYY-MM-DD}.log",
        rotation="00:00",  # New file at midnight
        compression="zip",  # Compress old logs
        retention="30 days",  # Keep logs for 30 days
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=settings.log_level,
    )
    
    # Error log file
    logger.add(
        "logs/errors_{time:YYYY-MM-DD}.log",
        rotation="00:00",
        compression="zip",
        retention="30 days",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="ERROR",
    )


# Initialize logger on import
setup_logger()
