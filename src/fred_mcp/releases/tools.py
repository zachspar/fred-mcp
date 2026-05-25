from fastmcp import FastMCP

from fred_mcp.common.tools import READ_ONLY_ANNOTATIONS, call_fred
from fred_mcp.common.types import (
    FredFilterVariable,
    FredReleaseOrderBy,
    FredSeriesSearchOrderBy,
    FredSortOrder,
    FredTagGroup,
    FredTagOrderBy,
)

releases_mcp = FastMCP("fred-releases")


@releases_mcp.tool(
    name="list_releases",
    description=(
        "List all FRED releases of economic data. "
        "Example: list_releases(limit=20)."
    ),
    annotations={**READ_ONLY_ANNOTATIONS, "title": "List FRED releases"},
)
def list_releases(
    realtime_start: str | None = None,
    realtime_end: str | None = None,
    limit: int | None = 1000,
    offset: int | None = 0,
    order_by: FredReleaseOrderBy | None = None,
    sort_order: FredSortOrder | None = "asc",
) -> dict:
    return call_fred(
        "get_releases",
        realtime_start=realtime_start,
        realtime_end=realtime_end,
        limit=limit,
        offset=offset,
        order_by=order_by,
        sort_order=sort_order,
    )


@releases_mcp.tool(
    name="list_release_dates",
    description=(
        "List release dates across all FRED releases. "
        "Example: list_release_dates(limit=50)."
    ),
    annotations={
        **READ_ONLY_ANNOTATIONS,
        "title": "List release dates for all releases",
    },
)
def list_release_dates(
    realtime_start: str | None = None,
    realtime_end: str | None = None,
    limit: int | None = 1000,
    offset: int | None = 0,
    order_by: FredReleaseOrderBy | None = None,
    sort_order: FredSortOrder | None = "asc",
    include_release_dates_with_no_data: bool | None = None,
) -> dict:
    return call_fred(
        "get_releases_dates",
        realtime_start=realtime_start,
        realtime_end=realtime_end,
        limit=limit,
        offset=offset,
        order_by=order_by,
        sort_order=sort_order,
        include_release_dates_with_no_data=include_release_dates_with_no_data,
    )


@releases_mcp.tool(
    name="get_release",
    description=(
        "Get metadata for a FRED release by release ID. "
        "Example: get_release(release_id=10)."
    ),
    annotations={**READ_ONLY_ANNOTATIONS, "title": "Get a FRED release"},
)
def get_release(
    release_id: int,
    realtime_start: str | None = None,
    realtime_end: str | None = None,
) -> dict:
    return call_fred(
        "get_release",
        release_id=release_id,
        realtime_start=realtime_start,
        realtime_end=realtime_end,
    )


@releases_mcp.tool(
    name="get_release_dates",
    description=(
        "Get release dates for a specific FRED release. "
        "Example: get_release_dates(release_id=10)."
    ),
    annotations={
        **READ_ONLY_ANNOTATIONS,
        "title": "Get dates for a release",
    },
)
def get_release_dates(
    release_id: int,
    realtime_start: str | None = None,
    realtime_end: str | None = None,
    limit: int | None = 10000,
    offset: int | None = 0,
    sort_order: FredSortOrder | None = "asc",
    include_release_dates_with_no_data: bool | None = None,
) -> dict:
    return call_fred(
        "get_release_dates",
        release_id=release_id,
        realtime_start=realtime_start,
        realtime_end=realtime_end,
        limit=limit,
        offset=offset,
        sort_order=sort_order,
        include_release_dates_with_no_data=include_release_dates_with_no_data,
    )


@releases_mcp.tool(
    name="get_release_series",
    description=(
        "List FRED series published in a release. "
        "Example: get_release_series(release_id=10, limit=20)."
    ),
    annotations={
        **READ_ONLY_ANNOTATIONS,
        "title": "List series in a release",
    },
)
def get_release_series(
    release_id: int,
    realtime_start: str | None = None,
    realtime_end: str | None = None,
    limit: int | None = 1000,
    offset: int | None = 0,
    order_by: FredSeriesSearchOrderBy | None = None,
    sort_order: FredSortOrder | None = "asc",
    filter_variable: FredFilterVariable | None = None,
    filter_value: str | None = None,
    tag_names: str | None = None,
    exclude_tag_names: str | None = None,
) -> dict:
    return call_fred(
        "get_release_series",
        release_id=release_id,
        realtime_start=realtime_start,
        realtime_end=realtime_end,
        limit=limit,
        offset=offset,
        order_by=order_by,
        sort_order=sort_order,
        filter_variable=filter_variable,
        filter_value=filter_value,
        tag_names=tag_names,
        exclude_tag_names=exclude_tag_names,
    )


@releases_mcp.tool(
    name="get_release_sources",
    description=(
        "Get sources that publish a FRED release. "
        "Example: get_release_sources(release_id=10)."
    ),
    annotations={
        **READ_ONLY_ANNOTATIONS,
        "title": "Get sources for a release",
    },
)
def get_release_sources(
    release_id: int,
    realtime_start: str | None = None,
    realtime_end: str | None = None,
) -> dict:
    return call_fred(
        "get_release_sources",
        release_id=release_id,
        realtime_start=realtime_start,
        realtime_end=realtime_end,
    )


@releases_mcp.tool(
    name="get_release_tags",
    description=(
        "Get tags for series in a FRED release. "
        "Example: get_release_tags(release_id=10)."
    ),
    annotations={
        **READ_ONLY_ANNOTATIONS,
        "title": "Get tags for a release",
    },
)
def get_release_tags(
    release_id: int,
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
        "get_release_tags",
        release_id=release_id,
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


@releases_mcp.tool(
    name="get_release_related_tags",
    description=(
        "Get related tags for tag(s) within a FRED release. "
        "Example: get_release_related_tags("
        "release_id=10, tag_names='usa')."
    ),
    annotations={
        **READ_ONLY_ANNOTATIONS,
        "title": "Get related tags for a release",
    },
)
def get_release_related_tags(
    release_id: int,
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
        "get_release_related_tags",
        release_id=release_id,
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


@releases_mcp.tool(
    name="get_release_tables",
    description=(
        "Get release tables (structured layouts) for a FRED release. "
        "Example: get_release_tables(release_id=53)."
    ),
    annotations={
        **READ_ONLY_ANNOTATIONS,
        "title": "Get tables for a release",
    },
)
def get_release_tables(
    release_id: int,
    element_id: int | None = None,
    include_observation_values: bool | None = None,
    observation_date: str | None = None,
) -> dict:
    return call_fred(
        "get_release_tables",
        release_id=release_id,
        element_id=element_id,
        include_observation_values=include_observation_values,
        observation_date=observation_date,
    )
