"""MCP stdio server implementation"""

import asyncio
from .app import server

async def _main_async():
    """Run the server in stdio mode."""
    await server.run_stdio_async()

def main():
    """Entry point for the stdio server."""
    return asyncio.run(_main_async()) 