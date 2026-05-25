from fastmcp import FastMCP

from fred_mcp.common.tools import READ_ONLY_ANNOTATIONS, call_fred
from fred_mcp.common.types import (
    FredAggregationMethod,
    FredFrequency,
    FredOutput,
    FredSearch,
    FredSeriesSearchOrderBy,
    FredSeriesUpdateFilter,
    FredSortOrder,
    FredTagGroup,
    FredTagOrderBy,
    FredUnit,
)

series_mcp = FastMCP("fred-series")


@series_mcp.tool(
    name="get_series",
    description=(
        "Get metadata for a FRED economic data series by series ID. "
        "Example: get_series(series_id='GNPCA')."
    ),
    annotations={**READ_ONLY_ANNOTATIONS, "title": "Get FRED series metadata"},
)
def get_series(
    series_id: str,
    realtime_start: str | None = None,
    realtime_end: str | None = None,
) -> dict:
    return call_fred(
        "get_series",
        series_id=series_id,
        realtime_start=realtime_start,
        realtime_end=realtime_end,
    )


@series_mcp.tool(
    name="get_series_categories",
    description=(
        "Get the categories that contain a FRED series. "
        "Example: get_series_categories(series_id='CPIAUCSL')."
    ),
    annotations={
        **READ_ONLY_ANNOTATIONS,
        "title": "Get categories for a FRED series",
    },
)
def get_series_categories(
    series_id: str,
    realtime_start: str | None = None,
    realtime_end: str | None = None,
) -> dict:
    return call_fred(
        "get_series_categories",
        series_id=series_id,
        realtime_start=realtime_start,
        realtime_end=realtime_end,
    )


@series_mcp.tool(
    name="get_series_observations",
    description=(
        "Get observations (data values) for a FRED series with optional "
        "unit transforms, frequency aggregation, and date filters. "
        "Example: get_series_observations(series_id='GNPCA', "
        "observation_start='2000-01-01')."
    ),
    annotations={
        **READ_ONLY_ANNOTATIONS,
        "title": "Get FRED series observations",
    },
)
def get_series_observations(
    series_id: str,
    realtime_start: str | None = None,
    realtime_end: str | None = None,
    limit: int | None = 100000,
    offset: int | None = 0,
    sort_order: FredSortOrder | None = "asc",
    observation_start: str | None = None,
    observation_end: str | None = None,
    units: FredUnit | None = "lin",
    frequency: FredFrequency | None = None,
    aggregation_method: FredAggregationMethod | None = None,
    output_type: FredOutput | None = 1,
    vintage_dates: str | None = None,
) -> dict:
    return call_fred(
        "get_series_observations",
        series_id=series_id,
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
    )


@series_mcp.tool(
    name="get_series_release",
    description=(
        "Get the release that publishes a FRED series. "
        "Example: get_series_release(series_id='CPIAUCSL')."
    ),
    annotations={
        **READ_ONLY_ANNOTATIONS,
        "title": "Get release for a FRED series",
    },
)
def get_series_release(
    series_id: str,
    realtime_start: str | None = None,
    realtime_end: str | None = None,
) -> dict:
    return call_fred(
        "get_series_release",
        series_id=series_id,
        realtime_start=realtime_start,
        realtime_end=realtime_end,
    )


@series_mcp.tool(
    name="search_series",
    description=(
        "Search FRED series by text or series ID with optional tag filters. "
        "Example: search_series(search_text='inflation', limit=10)."
    ),
    annotations={**READ_ONLY_ANNOTATIONS, "title": "Search FRED series"},
)
def search_series(
    search_text: str,
    search_type: FredSearch = "full_text",
    realtime_start: str | None = None,
    realtime_end: str | None = None,
    limit: int | None = 1000,
    offset: int | None = 0,
    order_by: FredSeriesSearchOrderBy | None = None,
    sort_order: FredSortOrder | None = "asc",
    filter_variable: str | None = None,
    filter_value: str | None = None,
    tag_names: str | None = None,
    exclude_tag_names: str | None = None,
) -> dict:
    return call_fred(
        "get_series_search",
        search_text=search_text,
        search_type=search_type,
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


@series_mcp.tool(
    name="search_series_tags",
    description=(
        "Get tags associated with a FRED series search, optionally filtered "
        "by tag name, group, or search text. "
        "Example: search_series_tags(series_search_text='gdp')."
    ),
    annotations={
        **READ_ONLY_ANNOTATIONS,
        "title": "Get tags for a FRED series search",
    },
)
def search_series_tags(
    series_search_text: str,
    realtime_start: str | None = None,
    realtime_end: str | None = None,
    tag_names: str | None = None,
    tag_group_id: FredTagGroup | None = None,
    tag_search_text: str | None = None,
    limit: int | None = 1000,
    offset: int | None = 0,
    order_by: FredTagOrderBy | None = "series_count",
    sort_order: FredSortOrder | None = "asc",
) -> dict:
    return call_fred(
        "get_series_search_tags",
        series_search_text=series_search_text,
        realtime_start=realtime_start,
        realtime_end=realtime_end,
        tag_names=tag_names,
        tag_group_id=tag_group_id,
        tag_search_text=tag_search_text,
        limit=limit,
        offset=offset,
        order_by=order_by,
        sort_order=sort_order,
    )


@series_mcp.tool(
    name="search_series_related_tags",
    description=(
        "Get related tags for one or more tags matching a FRED series search. "
        "Example: search_series_related_tags("
        "series_search_text='gdp', tag_names='usa')."
    ),
    annotations={
        **READ_ONLY_ANNOTATIONS,
        "title": "Get related tags for a FRED series search",
    },
)
def search_series_related_tags(
    series_search_text: str,
    tag_names: str,
    realtime_start: str | None = None,
    realtime_end: str | None = None,
    exclude_tag_names: str | None = None,
    tag_group_id: FredTagGroup | None = None,
    tag_search_text: str | None = None,
    limit: int | None = 1000,
    offset: int | None = 0,
    order_by: FredTagOrderBy | None = "series_count",
    sort_order: FredSortOrder | None = "asc",
) -> dict:
    return call_fred(
        "get_series_search_related_tags",
        series_search_text=series_search_text,
        tag_names=tag_names,
        realtime_start=realtime_start,
        realtime_end=realtime_end,
        exclude_tag_names=exclude_tag_names,
        tag_group_id=tag_group_id,
        tag_search_text=tag_search_text,
        limit=limit,
        offset=offset,
        order_by=order_by,
        sort_order=sort_order,
    )


@series_mcp.tool(
    name="get_series_tags",
    description=(
        "Get tags assigned to a FRED series. "
        "Example: get_series_tags(series_id='CPIAUCSL')."
    ),
    annotations={**READ_ONLY_ANNOTATIONS, "title": "Get tags for a FRED series"},
)
def get_series_tags(
    series_id: str,
    realtime_start: str | None = None,
    realtime_end: str | None = None,
    order_by: FredTagOrderBy | None = "series_count",
    sort_order: FredSortOrder | None = "asc",
) -> dict:
    return call_fred(
        "get_series_tags",
        series_id=series_id,
        realtime_start=realtime_start,
        realtime_end=realtime_end,
        order_by=order_by,
        sort_order=sort_order,
    )


@series_mcp.tool(
    name="get_series_updates",
    description=(
        "List FRED series sorted by when observations were last updated. "
        "Example: get_series_updates(filter_value='macro', limit=20)."
    ),
    annotations={**READ_ONLY_ANNOTATIONS, "title": "Get recently updated series"},
)
def get_series_updates(
    realtime_start: str | None = None,
    realtime_end: str | None = None,
    limit: int | None = 1000,
    offset: int | None = 0,
    filter_value: FredSeriesUpdateFilter | None = "all",
    start_time: str | None = None,
    end_time: str | None = None,
) -> dict:
    return call_fred(
        "get_series_updates",
        realtime_start=realtime_start,
        realtime_end=realtime_end,
        limit=limit,
        offset=offset,
        filter_value=filter_value,
        start_time=start_time,
        end_time=end_time,
    )


@series_mcp.tool(
    name="get_series_vintage_dates",
    description=(
        "Get vintage dates when a series was revised or new values were "
        "released. Example: get_series_vintage_dates(series_id='CPIAUCSL')."
    ),
    annotations={
        **READ_ONLY_ANNOTATIONS,
        "title": "Get vintage dates for a FRED series",
    },
)
def get_series_vintage_dates(
    series_id: str,
    realtime_start: str | None = None,
    realtime_end: str | None = None,
    limit: int | None = 10000,
    offset: int | None = 0,
    sort_order: FredSortOrder | None = "asc",
) -> dict:
    return call_fred(
        "get_series_vintagedates",
        series_id=series_id,
        realtime_start=realtime_start,
        realtime_end=realtime_end,
        limit=limit,
        offset=offset,
        sort_order=sort_order,
    )
