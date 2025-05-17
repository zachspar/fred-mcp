from fastmcp import FastMCP
from fred import FredAPI

mcp = FastMCP("FRED MCP Server")
fred = FredAPI("fred-api-key-1234")

@mcp.tool()
def hello_world(name: str) -> str:
    """
    A simple hello world tool.
    """
    return f"Hello, {name}!"

@mcp.resource(
    uri="resource://fred/series/observations/{series_id}",
    name="FredSeriesObservations",
    description="Read series observations",
    mime_type="application/json",
)
def get_fred_series_observations(series_id: str = "DFF") -> dict:
    """Get the observations or data values for an economic data series."""
    return {
        "series_id": series_id,
        "data": fred.get_series_observations(series_id)
    }


def main():
    """
    Main function to run the MCP server.
    """
    mcp.run(transport="streamable-http", port=8000, host="0.0.0.0")


if __name__ == "__main__":
    # main()
    import asyncio
    from fastmcp import Client

    client = Client(mcp)


    async def read_resource(name: str):
        async with client:
            result = await client.read_resource(f"resource://fred/series/observations/{name}")
            print(result)


    asyncio.run(read_resource("dff"))
