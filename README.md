# Screenshot MCP Server

An MCP server that provides screenshot capabilities for AI tools, allowing them to capture and process screen content.

## Overview

This MCP server enables AI tools to take screenshots of the user's screen, making it possible for AI assistants to see and analyze what the user is looking at. The server handles image capture, compression, and delivery in a format suitable for AI processing.

## Features

- Take full screen screenshots
- Automatic JPEG compression for efficient transfer
- Base64 encoded image data for reliable transmission
- Support for both stdio and SSE transport modes
- Configurable image quality and optimization
- Simple command-line interface for testing

## Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/codingthefuturewithai/screenshot_mcp_server.git
cd screenshot_mcp_server

# Install using UV (recommended)
uv pip install -e .

# Or using pip
pip install -e .
```

## Available Tools

### take_screenshot

Description: Takes a screenshot of the user's screen and returns it as a JPEG image.

Parameters: None

Returns:

- Image content in JPEG format, base64 encoded

## Usage

The server can be used in two ways:

### Command Line Client

```bash
# Take a screenshot and save it to a file
screenshot_mcp_server-client output.jpg
```

### Programmatic Usage

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async with stdio_client(StdioServerParameters(command="screenshot_mcp_server-server")) as (read, write):
    async with ClientSession(read, write) as session:
        result = await session.call_tool("take_screenshot")
        # Process the screenshot data...
```

## Requirements

- Python 3.10 or later (< 3.13)
- Dependencies:
  - mcp >= 1.0.0
  - pyautogui >= 0.9.54
  - Pillow >= 10.0.0
- Operating Systems: Linux, macOS, Windows

## Configuration

The server supports two transport modes:

- stdio (default): For command-line usage
- SSE: For web-based applications, runs on port 3001 by default

To run in SSE mode:

```bash
screenshot_mcp_server-server-sse --port 3001
```

## License

This project is licensed under the MIT License.

## Author

Tim Kitchens (timkitch@codingthefuture.ai)
