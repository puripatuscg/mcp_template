import logging
from fastmcp import FastMCP

logger = logging.getLogger(__name__)


def get_image_metadata(image_path: str) -> dict:
    """Get width, height, and format of a local image file.

    Args:
        image_path: Absolute or relative path to the image file
    """
    from PIL import Image
    img = Image.open(image_path)
    return {"width": img.width, "height": img.height, "format": img.format}


def resize_image(image_path: str, width: int, height: int, output_path: str) -> str:
    """Resize a local image and save to a new file.

    Args:
        image_path: Path to the source image
        width: Target width in pixels
        height: Target height in pixels
        output_path: Path where the resized image will be saved
    """
    from PIL import Image
    img = Image.open(image_path).resize((width, height))
    img.save(output_path)
    logger.info(f"Resized {image_path} → {output_path} ({width}x{height})")
    return output_path


def register(mcp: FastMCP) -> None:
    """Register all function tools with the MCP server."""
    mcp.tool()(get_image_metadata)
    mcp.tool()(resize_image)
