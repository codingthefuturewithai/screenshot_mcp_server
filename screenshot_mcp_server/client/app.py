"""MCP screenshot client implementation"""

import asyncio
import base64
import click
from pathlib import Path
from mcp import ClientSession, StdioServerParameters
from mcp.types import CallToolResult
from mcp.client.stdio import stdio_client
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


async def take_screenshot(output_path: Path) -> None:
    """
    Take a screenshot and save it to the specified path.

    Args:
        output_path: Path where the screenshot should be saved
    """
    # Create server parameters for stdio connection
    server_params = StdioServerParameters(
        command="screenshot_mcp_server-server",  # Use the installed script
        args=[],  # No additional args needed
        env=None,  # Optional environment variables
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # Call the screenshot tool and get the response
            result = await session.call_tool("take_screenshot")

            if isinstance(result, CallToolResult):
                if not result.content or not isinstance(result.content, list):
                    raise ValueError("Expected content to be a non-empty list")

                image_content = result.content[0]
                if not isinstance(image_content.data, str):
                    raise TypeError(
                        f"Expected string data, got {type(image_content.data)}"
                    )

                # Decode base64 string to bytes
                image_bytes = base64.b64decode(image_content.data)
                output_path.write_bytes(image_bytes)
            else:
                raise TypeError(f"Expected CallToolResult type, got {type(result)}")


@click.command()
@click.argument(
    "output_path", type=click.Path(dir_okay=False, writable=True, path_type=Path)
)
def main(output_path: Path):
    """Take a screenshot and save it to the specified path."""
    try:
        asyncio.run(take_screenshot(output_path))
        print(f"Screenshot saved to: {output_path}")
    except Exception as e:
        print(f"Error taking screenshot: {e}")
        raise


if __name__ == "__main__":
    main()
