import httpx
from config import settings


def get_client() -> httpx.AsyncClient:
    """Create a shared HTTP client with base URL and auth headers from settings."""
    return httpx.AsyncClient(
        base_url=settings.IMAGE_API_BASE_URL,
        headers={"X-API-Key": settings.IMAGE_API_KEY},
        timeout=30.0,
    )
