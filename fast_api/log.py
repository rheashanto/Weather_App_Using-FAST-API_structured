"""Logging configuration."""
import logging

from fast_api.settings import settings


def configure_logging() -> None:
    """Configure logging for the application."""
    logging.basicConfig(
        level=settings.log_level.value,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
