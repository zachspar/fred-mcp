import os

from ._types import *

from fastmcp import FastMCP
from fred import FredAPI, BaseFredAPIError


mcp = FastMCP("FRED MCP Server")
fred = FredAPI(os.environ.get("FRED_API_KEY"))


@mcp.tool(
    name="FRED Series Observations",
    description="Get FRED series observations.",
)
def get_fred_series_observations(
    series_id: str,
    realtime_start: str | None = None,
    realtime_end: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
    sort_order: FredSortOrder = "asc",
    observation_start: str | None = None,
    observation_end: str | None = None,
    units: FredUnit | None = None,
    frequency: FredFrequency | None = None,
    aggregation_method: FredAggregationMethod | None = None,
    output_type: FredOutputType = 1,
    vintage_dates: str | None = None,
) -> dict:
    """Get the observations or data values for an economic data series."""
    try:
        return {
            "series_id": series_id,
            "data": fred.get_series_observations(
                series_id,
                realtime_start=realtime_start,
                realtime_end=realtime_end,
                limit=limit,
                offset=offset,
                sort_order=sort_order,
                observation_start=observation_start,
                observation_end=observation_end,
                units=units,
                frequency=frequency,
                aggregation_method=aggregation_method,
                output_type=output_type,
                vintage_dates=vintage_dates,
                file_type="json",
            ),
        }
    except BaseFredAPIError as e:
        return {"error": e}


def main():
    """
    Main function to run the MCP server.
    """
    _TRANSPORT = os.environ.get("MCP_TRANSPORT", "sse")
    _PORT = os.environ.get("MCP_SERVER_PORT", "8000")
    _HOST = os.environ.get("MCP_SERVER_HOST", "localhost")
    mcp.run(transport=_TRANSPORT, port=_PORT, host=_HOST)


if __name__ == "__main__":
    main()
