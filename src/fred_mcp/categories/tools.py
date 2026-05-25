from fastmcp import FastMCP

from fred_mcp.common.tools import READ_ONLY_ANNOTATIONS, call_fred
from fred_mcp.common.types import (
    FredFilterVariable,
    FredSeriesSearchOrderBy,
    FredSortOrder,
    FredTagGroup,
    FredTagOrderBy,
)

categories_mcp = FastMCP("fred-categories")


@categories_mcp.tool(
    name="get_category",
    description=(
        "Get a FRED category by ID. Omit category_id for the root category. "
        "Example: get_category(category_id=125)."
    ),
    annotations={**READ_ONLY_ANNOTATIONS, "title": "Get a FRED category"},
)
def get_category(category_id: int | None = None) -> dict:
    return call_fred("get_category", category_id=category_id)


@categories_mcp.tool(
    name="get_category_children",
    description=(
        "Get child categories for a FRED category. "
        "Example: get_category_children(category_id=125)."
    ),
    annotations={
        **READ_ONLY_ANNOTATIONS,
        "title": "Get child categories",
    },
)
def get_category_children(
    category_id: int | None = None,
    realtime_start: str | None = None,
    realtime_end: str | None = None,
) -> dict:
    return call_fred(
        "get_category_children",
        category_id=category_id,
        realtime_start=realtime_start,
        realtime_end=realtime_end,
    )


@categories_mcp.tool(
    name="get_category_related",
    description=(
        "Get categories related to a FRED category. "
        "Example: get_category_related(category_id=125)."
    ),
    annotations={
        **READ_ONLY_ANNOTATIONS,
        "title": "Get related categories",
    },
)
def get_category_related(
    category_id: int,
    realtime_start: str | None = None,
    realtime_end: str | None = None,
) -> dict:
    return call_fred(
        "get_category_related",
        category_id=category_id,
        realtime_start=realtime_start,
        realtime_end=realtime_end,
    )


@categories_mcp.tool(
    name="get_category_series",
    description=(
        "List FRED series belonging to a category with optional filters. "
        "Example: get_category_series(category_id=125, limit=10)."
    ),
    annotations={
        **READ_ONLY_ANNOTATIONS,
        "title": "List series in a category",
    },
)
def get_category_series(
    category_id: int,
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
        "get_category_series",
        category_id=category_id,
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


@categories_mcp.tool(
    name="get_category_tags",
    description=(
        "Get tags for series in a FRED category. "
        "Example: get_category_tags(category_id=125)."
    ),
    annotations={
        **READ_ONLY_ANNOTATIONS,
        "title": "Get tags for a category",
    },
)
def get_category_tags(
    category_id: int,
    realtime_start: str | None = None,
    realtime_end: str | None = None,
    limit: int | None = 1000,
    offset: int | None = 0,
    order_by: FredTagOrderBy | None = "series_count",
    sort_order: FredSortOrder | None = "asc",
    filter_variable: FredFilterVariable | None = None,
    filter_value: str | None = None,
    tag_names: str | None = None,
    tag_group_id: FredTagGroup | None = None,
    search_text: str | None = None,
) -> dict:
    return call_fred(
        "get_category_tags",
        category_id=category_id,
        realtime_start=realtime_start,
        realtime_end=realtime_end,
        limit=limit,
        offset=offset,
        order_by=order_by,
        sort_order=sort_order,
        filter_variable=filter_variable,
        filter_value=filter_value,
        tag_names=tag_names,
        tag_group_id=tag_group_id,
        search_text=search_text,
    )


@categories_mcp.tool(
    name="get_category_related_tags",
    description=(
        "Get related tags for tag(s) within a FRED category. "
        "Example: get_category_related_tags("
        "category_id=125, tag_names='usa')."
    ),
    annotations={
        **READ_ONLY_ANNOTATIONS,
        "title": "Get related tags for a category",
    },
)
def get_category_related_tags(
    category_id: int,
    tag_names: str,
    realtime_start: str | None = None,
    realtime_end: str | None = None,
    limit: int | None = 1000,
    offset: int | None = 0,
    order_by: FredTagOrderBy | None = "series_count",
    sort_order: FredSortOrder | None = "asc",
    filter_variable: FredFilterVariable | None = None,
    filter_value: str | None = None,
    exclude_tag_names: str | None = None,
    tag_group_id: FredTagGroup | None = None,
    search_text: str | None = None,
) -> dict:
    return call_fred(
        "get_category_related_tags",
        category_id=category_id,
        tag_names=tag_names,
        realtime_start=realtime_start,
        realtime_end=realtime_end,
        limit=limit,
        offset=offset,
        order_by=order_by,
        sort_order=sort_order,
        filter_variable=filter_variable,
        filter_value=filter_value,
        exclude_tag_names=exclude_tag_names,
        tag_group_id=tag_group_id,
        search_text=search_text,
    )
