import logging
from fastmcp import FastMCP
from .client import get_client

logger = logging.getLogger(__name__)


async def detect_objects(image_url: str, model: str = "yolo") -> dict:
    """Detect objects in an image using the image platform API.

    Args:
        image_url: URL of the image to analyze
        model: Detection model to use (e.g. "yolo", "faster-rcnn")
    """
    async with get_client() as client:
        r = await client.post("/detect", json={"image_url": image_url, "model": model})
        r.raise_for_status()
        logger.info(f"detect_objects: {image_url} model={model} status={r.status_code}")
        return r.json()


async def classify_image(image_url: str, top_k: int = 5) -> dict:
    """Classify an image and return top-k class predictions.

    Args:
        image_url: URL of the image to classify
        top_k: Number of top predictions to return (default: 5)
    """
    async with get_client() as client:
        r = await client.post("/classify", json={"image_url": image_url, "top_k": top_k})
        r.raise_for_status()
        logger.info(f"classify_image: {image_url} top_k={top_k} status={r.status_code}")
        return r.json()


def register(mcp: FastMCP) -> None:
    """Register all API tools with the MCP server."""
    mcp.tool()(detect_objects)
    mcp.tool()(classify_image)
