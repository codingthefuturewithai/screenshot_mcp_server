"""MCP SSE server implementation"""

import asyncio
import click
from .app import server

async def _main_async(port: int):
    """Run the server in SSE mode."""
    server.settings.port = port
    await server.run_sse_async()

@click.command()
@click.option("--port", default=3001, help="Port to listen on")
def main(port: int):
    """Entry point for the SSE server."""
    return asyncio.run(_main_async(port)) 