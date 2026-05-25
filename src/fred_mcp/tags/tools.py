from fastmcp import FastMCP

from fred_mcp.common.tools import READ_ONLY_ANNOTATIONS, call_fred
from fred_mcp.common.types import (
    FredSeriesSearchOrderBy,
    FredSortOrder,
    FredTagGroup,
    FredTagOrderBy,
)

tags_mcp = FastMCP("fred-tags")


@tags_mcp.tool(
    name="list_tags",
    description=(
        "Search or list FRED tags with optional filters. "
        "Example: list_tags(search_text='gdp', limit=20)."
    ),
    annotations={**READ_ONLY_ANNOTATIONS, "title": "List FRED tags"},
)
def list_tags(
    realtime_start: str | None = None,
    realtime_end: str | None = None,
    tag_names: str | None = None,
    tag_group_id: FredTagGroup | None = None,
    search_text: str | None = None,
    limit: int | None = 1000,
    offset: int | None = 0,
    order_by: FredTagOrderBy | None = "series_count",
    sort_order: FredSortOrder | None = "asc",
) -> dict:
    return call_fred(
        "get_tags",
        realtime_start=realtime_start,
        realtime_end=realtime_end,
        tag_names=tag_names,
        tag_group_id=tag_group_id,
        search_text=search_text,
        limit=limit,
        offset=offset,
        order_by=order_by,
        sort_order=sort_order,
    )


@tags_mcp.tool(
    name="get_related_tags",
    description=(
        "Get tags related to one or more FRED tags. "
        "Example: get_related_tags(tag_names='usa;gdp')."
    ),
    annotations={**READ_ONLY_ANNOTATIONS, "title": "Get related FRED tags"},
)
def get_related_tags(
    tag_names: str,
    realtime_start: str | None = None,
    realtime_end: str | None = None,
    exclude_tag_names: str | None = None,
    tag_group_id: FredTagGroup | None = None,
    search_text: str | None = None,
    limit: int | None = 1000,
    offset: int | None = 0,
    order_by: FredTagOrderBy | None = "series_count",
    sort_order: FredSortOrder | None = "asc",
) -> dict:
    return call_fred(
        "get_related_tags",
        tag_names=tag_names,
        realtime_start=realtime_start,
        realtime_end=realtime_end,
        exclude_tag_names=exclude_tag_names,
        tag_group_id=tag_group_id,
        search_text=search_text,
        limit=limit,
        offset=offset,
        order_by=order_by,
        sort_order=sort_order,
    )


@tags_mcp.tool(
    name="get_tags_series",
    description=(
        "List FRED series matching one or more tags. "
        "Example: get_tags_series(tag_names='gdp;usa', limit=10)."
    ),
    annotations={
        **READ_ONLY_ANNOTATIONS,
        "title": "List series by tags",
    },
)
def get_tags_series(
    tag_names: str,
    realtime_start: str | None = None,
    realtime_end: str | None = None,
    exclude_tag_names: str | None = None,
    limit: int | None = 1000,
    offset: int | None = 0,
    order_by: FredSeriesSearchOrderBy | None = None,
    sort_order: FredSortOrder | None = "asc",
) -> dict:
    return call_fred(
        "get_tags_series",
        tag_names=tag_names,
        realtime_start=realtime_start,
        realtime_end=realtime_end,
        exclude_tag_names=exclude_tag_names,
        limit=limit,
        offset=offset,
        order_by=order_by,
        sort_order=sort_order,
    )
