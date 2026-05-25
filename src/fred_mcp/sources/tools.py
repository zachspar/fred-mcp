from fastmcp import FastMCP

from fred_mcp.common.tools import READ_ONLY_ANNOTATIONS, call_fred
from fred_mcp.common.types import FredSortOrder, FredSourceOrderBy

sources_mcp = FastMCP("fred-sources")


@sources_mcp.tool(
    name="list_sources",
    description=(
        "List FRED data sources (providers). Example: list_sources(limit=20)."
    ),
    annotations={**READ_ONLY_ANNOTATIONS, "title": "List FRED sources"},
)
def list_sources(
    realtime_start: str | None = None,
    realtime_end: str | None = None,
    limit: int | None = 1000,
    offset: int | None = 0,
    order_by: FredSourceOrderBy | None = None,
    sort_order: FredSortOrder | None = "asc",
) -> dict:
    return call_fred(
        "get_sources",
        realtime_start=realtime_start,
        realtime_end=realtime_end,
        limit=limit,
        offset=offset,
        order_by=order_by,
        sort_order=sort_order,
    )


@sources_mcp.tool(
    name="get_source",
    description=(
        "Get metadata for a FRED source by source ID. "
        "Example: get_source(source_id=1)."
    ),
    annotations={**READ_ONLY_ANNOTATIONS, "title": "Get a FRED source"},
)
def get_source(
    source_id: int,
    realtime_start: str | None = None,
    realtime_end: str | None = None,
) -> dict:
    return call_fred(
        "get_source",
        source_id=source_id,
        realtime_start=realtime_start,
        realtime_end=realtime_end,
    )


@sources_mcp.tool(
    name="get_source_releases",
    description=(
        "List releases published by a FRED source. "
        "Example: get_source_releases(source_id=1, limit=20)."
    ),
    annotations={
        **READ_ONLY_ANNOTATIONS,
        "title": "List releases for a source",
    },
)
def get_source_releases(
    source_id: int,
    realtime_start: str | None = None,
    realtime_end: str | None = None,
    limit: int | None = 1000,
    offset: int | None = 0,
    order_by: FredSourceOrderBy | None = None,
    sort_order: FredSortOrder | None = "asc",
) -> dict:
    return call_fred(
        "get_source_releases",
        source_id=source_id,
        realtime_start=realtime_start,
        realtime_end=realtime_end,
        limit=limit,
        offset=offset,
        order_by=order_by,
        sort_order=sort_order,
    )
