"""Screenshot tool implementation for MCP server"""

import io
from mcp.server.fastmcp.utilities.types import Image


def take_screenshot() -> Image:
    """
    Take a screenshot of the user's screen and return it as an image. Use
    this tool anytime the user wants to look at something they're doing.
    """
    import pyautogui

    buffer = io.BytesIO()
    # if the file exceeds ~1MB, it will be rejected by Claude
    screenshot = pyautogui.screenshot()
    screenshot.convert("RGB").save(buffer, format="JPEG", quality=60, optimize=True)

    return Image(data=buffer.getvalue(), format="jpeg")
