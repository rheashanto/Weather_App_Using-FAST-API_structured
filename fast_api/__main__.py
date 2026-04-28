"""Entry point for running the application."""
import uvicorn

from fast_api.settings import settings


def main() -> None:
    """Run the application."""
    uvicorn.run(
        "fast_api.web.application:get_app",
        workers=settings.workers_count,
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        factory=True,
    )


if __name__ == "__main__":
    main()
