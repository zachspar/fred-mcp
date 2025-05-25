import os

from fred_mcp.common.types import *

from fastmcp import FastMCP
from fred import FredAPI, BaseFredAPIError


__all__ = ["series_mcp"]

series_mcp = FastMCP("FRED Series MCP Server")
fred = FredAPI(os.environ.get("FRED_API_KEY"))


@series_mcp.tool(
    name="FREDSeries",
    description="Get an economic data series.",
    annotations={
        "title": "Get FRED series.",
        "readOnlyHint": True,
        "openWorldHint": True,
    },
)
def get_series(
    series_id: str,
    realtime_start: str | None = None,
    realtime_end: str | None = None,
) -> dict:
    """
    Get FRED series.
    """
    try:
        return {
            "series_id": series_id,
            "data": fred.get_series(
                series_id,
                realtime_start=realtime_start,
                realtime_end=realtime_end,
                file_type="json",
            ),
        }
    except BaseFredAPIError as e:
        return {"error": e}


@series_mcp.tool(
    name="FREDSeriesCategories",
    description="Get the categories for an economic data series.",
    annotations={
        "title": "Get FRED series categories.",
        "readOnlyHint": True,
        "openWorldHint": True,
    },
)
def get_series_categories(
    series_id: str,
    realtime_start: str | None = None,
    realtime_end: str | None = None,
) -> dict:
    """
    Get FRED series categories.
    """
    try:
        return {
            "series_id": series_id,
            "data": fred.get_series_categories(
                series_id,
                realtime_start=realtime_start,
                realtime_end=realtime_end,
                file_type="json",
            ),
        }
    except BaseFredAPIError as e:
        return {"error": e}


@series_mcp.tool(
    name="FREDSeriesObservations",
    description="Get the observations or data values for an economic data series.",
    annotations={
        "title": "Get FRED series observations.",
        "readOnlyHint": True,
        "openWorldHint": True,
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
    """Get FRED series observations."""
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


@series_mcp.tool(
    name="FREDSeriesRelease",
    description="Get the release for an economic data series.",
    annotations={
        "title": "Get FRED series release.",
        "readOnlyHint": True,
        "openWorldHint": True,
    },
)
def get_series_release(
    series_id: str,
    realtime_start: str | None = None,
    realtime_end: str | None = None,
) -> dict:
    """
    Get FRED series release.
    """
    try:
        return {
            "series_id": series_id,
            "data": fred.get_series_release(
                series_id,
                realtime_start=realtime_start,
                realtime_end=realtime_end,
                file_type="json",
            ),
        }
    except BaseFredAPIError as e:
        return {"error": e}


@series_mcp.tool(
    name="FREDSeriesSearch",
    description="Get economic data series that match search text.",
    annotations={
        "title": "Get FRED series search by text.",
        "readOnlyHint": True,
        "openWorldHint": True,
    },
)
def get_series_search(
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
    """Get FRED series search by text."""
    try:
        return {
            "search_text": search_text,
            "data": fred.get_series_search(
                search_text,
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
                file_type="json",
            ),
        }
    except BaseFredAPIError as e:
        return {"error": e}


@series_mcp.tool(
    name="FREDSeriesSearchTags",
    description="Get the FRED tags for a series search. Optionally, filter results by tag name, tag group, or tag search.",
    annotations={
        "title": "Get FRED series search tags.",
        "readOnlyHint": True,
        "openWorldHint": True,
    },
)
def get_series_search_tags(
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
    """
    Get tags for FRED series search.
    """
    try:
        return {
            "series_search_text": series_search_text,
            "data": fred.get_series_search_tags(
                series_search_text,
                realtime_start=realtime_start,
                realtime_end=realtime_end,
                tag_names=tag_names,
                tag_group_id=tag_group_id,
                tag_search_text=tag_search_text,
                limit=limit,
                offset=offset,
                order_by=order_by,
                sort_order=sort_order,
                file_type="json",
            ),
        }
    except BaseFredAPIError as e:
        return {"error": str(e)}


@series_mcp.tool(
    name="FREDSeriesSearchRelatedTags",
    description="Get the related FRED tags for one or more FRED tags matching a series search.",
    annotations={
        "title": "Get FRED series search related tags.",
        "readOnlyHint": True,
        "openWorldHint": True,
    },
)
def get_series_search_related_tags(
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
    """
    Get related tags for FRED series search.
    """
    try:
        return {
            "series_search_text": series_search_text,
            "tag_names": tag_names,
            "data": fred.get_series_search_related_tags(
                series_search_text,
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
                file_type="json",
            ),
        }
    except BaseFredAPIError as e:
        return {"error": str(e)}


@series_mcp.tool(
    name="FREDSeriesTags",
    description="Get the FRED tags for a series.",
    annotations={
        "title": "Get FRED series tags.",
        "readOnlyHint": True,
        "openWorldHint": True,
    },
)
def get_series_tags(
    series_id: str,
    realtime_start: str | None = None,
    realtime_end: str | None = None,
    order_by: FredTagOrderBy | None = "series_count",
    sort_order: FredSortOrder | None = "asc",
) -> dict:
    """
    Get tags for a FRED series.
    """
    try:
        return {
            "series_id": series_id,
            "data": fred.get_series_tags(
                series_id,
                realtime_start=realtime_start,
                realtime_end=realtime_end,
                order_by=order_by,
                sort_order=sort_order,
                file_type="json",
            ),
        }
    except BaseFredAPIError as e:
        return {"error": str(e)}


@series_mcp.tool(
    name="FREDSeriesUpdates",
    description="Get economic data series sorted by when observations were updated on FRED.",
    annotations={
        "title": "Get FRED series updates.",
        "readOnlyHint": True,
        "openWorldHint": True,
    },
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
    """
    Get updates for FRED economic data series.
    """
    try:
        return {
            "data": fred.get_series_updates(
                realtime_start=realtime_start,
                realtime_end=realtime_end,
                limit=limit,
                offset=offset,
                filter_value=filter_value,
                start_time=start_time,
                end_time=end_time,
                file_type="json",
            ),
        }
    except BaseFredAPIError as e:
        return {"error": str(e)}


@series_mcp.tool(
    name="FREDSeriesVintageDates",
    description="Get the dates in history when a series' data values were revised or new data values were released.",
    annotations={
        "title": "Get FRED series vintage dates.",
        "readOnlyHint": True,
        "openWorldHint": True,
    },
)
def get_series_vintagedates(
    series_id: str,
    realtime_start: str | None = None,
    realtime_end: str | None = None,
    limit: int | None = 10000,
    offset: int | None = 0,
    sort_order: FredSortOrder | None = "asc",
) -> dict:
    """
    Get vintage dates for a FRED series.
    """
    try:
        return {
            "series_id": series_id,
            "data": fred.get_series_vintagedates(
                series_id,
                realtime_start=realtime_start,
                realtime_end=realtime_end,
                limit=limit,
                offset=offset,
                sort_order=sort_order,
                file_type="json",
            ),
        }
    except BaseFredAPIError as e:
        return {"error": str(e)}
