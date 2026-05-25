from fred_mcp.categories.tools import categories_mcp
from fred_mcp.config import get_settings
from fred_mcp.releases.tools import releases_mcp
from fred_mcp.series.tools import series_mcp
from fred_mcp.sources.tools import sources_mcp
from fred_mcp.tags.tools import tags_mcp

from fastmcp import FastMCP

mcp = FastMCP("fred-mcp")

mcp.mount(series_mcp)
mcp.mount(categories_mcp)
mcp.mount(releases_mcp)
mcp.mount(sources_mcp)
mcp.mount(tags_mcp)


@mcp.prompt(
    name="fred_research_workflow",
    description=(
        "Guide for researching economic data with FRED: search series, "
        "inspect metadata, then fetch observations."
    ),
)
def fred_research_workflow(topic: str) -> str:
    return (
        f"Research economic data about '{topic}' using FRED:\n"
        "1. search_series(search_text=...) to find candidate series IDs.\n"
        "2. get_series(series_id=...) for metadata, units, and frequency.\n"
        "3. get_series_observations(series_id=...) for the actual data.\n"
        "4. Optionally use get_series_release or get_category_series to "
        "explore related releases and categories."
    )


def main() -> None:
    settings = get_settings()
    settings.validate_for_transport()

    if settings.transport == "stdio":
        mcp.run(transport=settings.transport)
    else:
        mcp.run(
            transport=settings.transport,
            host=settings.host,
            port=settings.port,
        )


if __name__ == "__main__":
    main()
