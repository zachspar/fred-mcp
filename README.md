# Federal Reserve Economic Data MCP Server

> [!NOTE]
> This open-source project is not affiliated with, sponsored by, or endorsed by the *Federal Reserve* or the *Federal Reserve Bank of St. Louis*. "FRED" is a registered trademark of the *Federal Reserve Bank of St. Louis*, used here for descriptive purposes only.

A production-grade [Model Context Protocol](https://modelcontextprotocol.io/) server for [FRED®](https://fred.stlouisfed.org/) economic data. Covers all **31 endpoints** exposed by [fred-py-api](https://github.com/zachspar/fred-py-api).

## Features

- Full FRED API v1 coverage: series, categories, releases, sources, and tags
- FastMCP 3.x with structured tool output and proper `ToolError` handling
- Dual-mode credentials: environment variable (stdio) or per-client HTTP header (remote BYOK)
- Transports: `stdio`, `streamable-http`, and `sse`
- Docker image published to GHCR

## Installation

```bash
pip install fred-mcp
```

Requires Python 3.10+.

Get a free FRED API key at [fredaccount.stlouisfed.org/apikey](https://fredaccount.stlouisfed.org/apikey).

## Quick start

### Local (stdio)

Best for Claude Desktop, mcphost, and other clients that spawn a local process.

```bash
export FRED_API_KEY=your_api_key
fred-mcp
```

### Remote HTTP (bring your own key)

Deploy the server publicly and let each client send their own FRED API key via header. **No shared server-side key is required.**

Clients connect with `streamable-http` and send:

```http
X-FRED-API-Key: your_fred_api_key
```

Example with the FastMCP client:

```python
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport

transport = StreamableHttpTransport(
    "https://your-host.example.com/mcp",
    headers={"X-FRED-API-Key": "your_fred_api_key"},
)
async with Client(transport=transport) as client:
  await client.ping()
```

For public internet deployment, terminate TLS at a reverse proxy (nginx, Caddy, Cloudflare). Do not expose plain HTTP with API keys.

### Optional server-side fallback key

Set `FRED_API_KEY` on the server for clients that cannot send custom headers. Header takes precedence when both are present.

| Variable | Default | Description |
|----------|---------|-------------|
| `FRED_API_KEY` | — | FRED API key (required for stdio; optional HTTP fallback) |
| `FRED_API_KEY_HEADER` | `X-FRED-API-Key` | HTTP header name for BYOK |
| `MCP_SERVER_TRANSPORT` | `stdio` | `stdio`, `streamable-http`, or `sse` |
| `MCP_SERVER_HOST` | `localhost` | Bind host for HTTP transports |
| `MCP_SERVER_PORT` | `8000` | Bind port for HTTP transports |

## Client integration

### Claude Desktop

```json
{
  "mcpServers": {
    "fred-mcp": {
      "command": "fred-mcp",
      "env": {
        "FRED_API_KEY": "<your api key>"
      }
    }
  }
}
```

### mcphost

```json
{
  "mcpServers": {
    "fred": {
      "command": "fred-mcp",
      "env": {
        "FRED_API_KEY": "<your api key>"
      }
    }
  }
}
```

### Docker (streamable-http)

Run the server:

```bash
docker run -d -p 8000:8000 \
  --name fred-mcp-server \
  ghcr.io/zachspar/fred-mcp/fred-mcp-server:latest
```

Connect with your FRED key in the header (see remote HTTP example above).

For stdio via Docker:

```json
{
  "command": "docker",
  "args": [
    "run", "-i", "--rm",
    "-e", "MCP_SERVER_TRANSPORT=stdio",
    "-e", "FRED_API_KEY=your_api_key",
    "ghcr.io/zachspar/fred-mcp/fred-mcp-server:latest"
  ]
}
```

## Tools (31)

### Series

| Tool | Description |
|------|-------------|
| `get_series` | Series metadata |
| `get_series_categories` | Categories for a series |
| `get_series_observations` | Data values / observations |
| `get_series_release` | Release that publishes a series |
| `search_series` | Search series by text or ID |
| `search_series_tags` | Tags for a series search |
| `search_series_related_tags` | Related tags for a series search |
| `get_series_tags` | Tags on a series |
| `get_series_updates` | Recently updated series |
| `get_series_vintage_dates` | Vintage / revision dates |

### Categories

| Tool | Description |
|------|-------------|
| `get_category` | Category metadata |
| `get_category_children` | Child categories |
| `get_category_related` | Related categories |
| `get_category_series` | Series in a category |
| `get_category_tags` | Tags in a category |
| `get_category_related_tags` | Related tags in a category |

### Releases

| Tool | Description |
|------|-------------|
| `list_releases` | All releases |
| `list_release_dates` | Release dates across releases |
| `get_release` | Release metadata |
| `get_release_dates` | Dates for one release |
| `get_release_series` | Series in a release |
| `get_release_sources` | Sources for a release |
| `get_release_tags` | Tags for a release |
| `get_release_related_tags` | Related tags for a release |
| `get_release_tables` | Release tables |

### Sources

| Tool | Description |
|------|-------------|
| `list_sources` | All data sources |
| `get_source` | Source metadata |
| `get_source_releases` | Releases from a source |

### Tags

| Tool | Description |
|------|-------------|
| `list_tags` | Search / list tags |
| `get_related_tags` | Related tags |
| `get_tags_series` | Series matching tags |

## Migration from 0.x

Version 1.0.0 renames tools to snake_case and upgrades to FastMCP 3.x.

| Old name (0.x) | New name (1.0) |
|----------------|----------------|
| `FREDSeries` | `get_series` |
| `FREDSeriesCategories` | `get_series_categories` |
| `FREDSeriesObservations` | `get_series_observations` |
| `FREDSeriesRelease` | `get_series_release` |
| `FREDSeriesSearch` | `search_series` |
| `FREDSeriesSearchTags` | `search_series_tags` |
| `FREDSeriesSearchRelatedTags` | `search_series_related_tags` |
| `FREDSeriesTags` | `get_series_tags` |
| `FREDSeriesUpdates` | `get_series_updates` |
| `FREDSeriesVintageDates` | `get_series_vintage_dates` |

21 additional tools were added for categories, releases, sources, and tags.

Error responses now use MCP `ToolError` (`isError: true`) instead of `{"error": ...}` payloads.

## Development

```bash
python3.13 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
ruff check src tests
```

## License

MIT
