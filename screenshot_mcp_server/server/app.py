"""MCP server implementation with Screenshot tool"""

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.utilities.types import Image
import logging
import sys
import asyncio
import click

from screenshot_mcp_server.tools.screenshot import take_screenshot

# Configure logging to write to stderr
logging.basicConfig(
    stream=sys.stderr,
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger("screenshot_mcp_server.mcp")


def create_mcp_server() -> FastMCP:
    """Create and configure the MCP server instance"""
    server = FastMCP(
        "Screenshot MCP Server",
        host="localhost",
        port=3001,
        dependencies=["pyautogui", "Pillow"],
    )

    # Register all tools with the server
    register_tools(server)

    return server


def register_tools(mcp_server: FastMCP) -> None:
    """Register all MCP tools with the server"""

    @mcp_server.tool(
        name="take_screenshot",
        description="Take a screenshot of the user's screen and return it as an image",
    )
    def screenshot_tool() -> Image:
        """Wrapper around the screenshot tool implementation"""
        return take_screenshot()


# Create a server instance that can be imported by the MCP CLI
server = create_mcp_server()


@click.command()
@click.option("--port", default=3001, help="Port to listen on for SSE")
@click.option(
    "--transport",
    type=click.Choice(["stdio", "sse"]),
    default="stdio",
    help="Transport type (stdio or sse)",
)
def main(port: int, transport: str) -> int:
    """Run the server with specified transport."""
    try:
        if transport == "stdio":
            asyncio.run(server.run_stdio_async())
        else:
            server.settings.port = port
            asyncio.run(server.run_sse_async())
        return 0
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
        return 0
    except Exception as e:
        logger.error(f"Failed to start server: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
