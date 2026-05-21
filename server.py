import logging
from fastmcp import FastMCP
from config import settings
from tools.function_tools.image_utils import register as register_func_tools
from tools.api_tools.image_platform import register as register_api_tools
from tools.function_tools.math_utils import register as register_math_tools
from tools.api_tools.math_platform import register as register_math_api_tools

logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s %(levelname)s %(name)s — %(message)s",
)

mcp = FastMCP("Image Platform MCP")
register_func_tools(mcp)
register_api_tools(mcp)
register_math_tools(mcp)
register_math_api_tools(mcp)

if __name__ == "__main__":
    if settings.TRANSPORT == "http":
        mcp.run(transport="streamable-http", host=settings.HOST, port=settings.PORT)
    else:
        mcp.run()
