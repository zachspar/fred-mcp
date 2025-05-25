import os
import asyncio
from typing import Literal

from fastmcp import FastMCP

from fred_mcp.series.mcp import series_mcp


mcp = FastMCP("FRED MCP Server")


async def import_servers():
    """
    Import mcp sub-servers.
    """
    await mcp.import_server("series", series_mcp)


def main():
    """
    Main function to run the MCP server.
    """
    asyncio.run(import_servers())

    _TRANSPORT: Literal["stdio", "sse", "streamable-http"] = os.environ.get(
        "MCP_SERVER_TRANSPORT", "stdio"
    )
    _PORT = os.environ.get("MCP_SERVER_PORT", "8000")
    _HOST = os.environ.get("MCP_SERVER_HOST", "localhost")

    if _TRANSPORT == "stdio":
        mcp.run(transport=_TRANSPORT)
    else:
        if not _PORT.isnumeric():
            raise ValueError(f"Invalid port number: {_PORT}")

        # if transport is not stdio, we need to set the host and port for server
        mcp.run(transport=_TRANSPORT, port=int(_PORT), host=_HOST)


if __name__ == "__main__":
    main()
