# Federal Reserve Economic Data MCP Server

> [!NOTE]
> This open-source project is not affiliated with, sponsored by, or endorsed by the *Federal Reserve* or the *Federal Reserve Bank of St. Louis*. "FRED" is a registered trademark of the *Federal Reserve Bank of St. Louis*, used here for descriptive purposes only.

A production-grade [Model Context Protocol](https://modelcontextprotocol.io/) server for [FRED®](https://fred.stlouisfed.org/) economic data. Covers all **31 endpoints** exposed by [fred-py-api](https://github.com/zachspar/fred-py-api).

## Features

- Full FRED API v1 coverage: series, categories, releases, sources, and tags
- FastMCP 4 with structured tool output and proper `ToolError` handling
- Dual-mode credentials: environment variable (stdio) or per-client HTTP header (remote BYOK)
- Transports: `stdio`, `streamable-http`, and `sse`
- Docker image published to GHCR

## Installation

```bash
pip install fred-mcp
```

Requires Python 3.10+.

Get a free FRED API key at [fredaccount.stlouisfed.org/apikey](https://fredaccount.stlouisfed.org/apikey).

## Setup

### Remote hosted server (recommended)

Use the public hosted server with **bring your own key** (BYOK): no install and no shared server-side API key. Each client sends its own FRED API key in the `X-FRED-API-Key` header.

Transport: **streamable HTTP**. Endpoint: `https://fred-mcp-prod.fly.dev/mcp`.

Add this to your MCP client's configuration file and restart the client:

```json
{
  "mcpServers": {
    "fred-mcp": {
      "url": "https://fred-mcp-prod.fly.dev/mcp",
      "headers": {
        "X-FRED-API-Key": "<your fred api key>"
      }
    }
  }
}
```

Programmatic example with the FastMCP client:

```python
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport

transport = StreamableHttpTransport(
    "https://fred-mcp-prod.fly.dev/mcp",
    headers={"X-FRED-API-Key": "your_fred_api_key"},
)
async with Client(transport=transport) as client:
    await client.list_tools()
```

### Local (stdio)

For clients that spawn a local process, install [fred-mcp](#installation) and use:

```json
{
  "mcpServers": {
    "fred-mcp": {
      "command": "fred-mcp",
      "env": {
        "FRED_API_KEY": "<your fred api key>"
      }
    }
  }
}
```

Or run directly from the terminal:

```bash
export FRED_API_KEY=your_api_key
fred-mcp
```

### Self-hosted HTTP

Deploy your own instance and use the same `url` + `headers` configuration, substituting your host for the endpoint above. **No shared server-side key is required** when clients send `X-FRED-API-Key`.

For public internet deployment, terminate TLS at a reverse proxy (nginx, Caddy, Cloudflare). Do not expose plain HTTP with API keys.

#### Docker

Run the server:

```bash
docker run -d -p 8000:8000 \
  --name fred-mcp-server \
  ghcr.io/zachspar/fred-mcp/fred-mcp-server:latest
```

The image is published only when a GitHub Release is published. That push tags `latest`, the release's git tag, and the released commit SHA.

Connect with your FRED API key in the `X-FRED-API-Key` header (same JSON shape as the remote hosted example, with `url` set to your deployment).

For stdio via Docker:

```json
{
  "mcpServers": {
    "fred-mcp": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-e", "MCP_SERVER_TRANSPORT=stdio",
        "-e", "FRED_API_KEY=<your fred api key>",
        "ghcr.io/zachspar/fred-mcp/fred-mcp-server:latest"
      ]
    }
  }
}
```

#### Optional server-side fallback key

Set `FRED_API_KEY` on the server for clients that cannot send custom headers. Header takes precedence when both are present.

| Variable | Default | Description |
|----------|---------|-------------|
| `FRED_API_KEY` | — | FRED API key (required for stdio; optional HTTP fallback) |
| `FRED_API_KEY_HEADER` | `X-FRED-API-Key` | HTTP header name for BYOK |
| `MCP_SERVER_TRANSPORT` | `stdio` | `stdio`, `streamable-http`, or `sse` |
| `MCP_SERVER_HOST` | `localhost` | Bind host for HTTP transports |
| `MCP_SERVER_PORT` | `8000` | Bind port for HTTP transports |
| `MCP_LOG_LEVEL` | `INFO` | Level for structlog JSON lines |
| `MCP_LOG_MAX_BODY` | `65536` | Max bytes of a tool's arguments or result kept in one log line. `0` keeps the full payload |

Each MCP tool call writes one JSON line to stderr. The line includes the tool name, the arguments, the result or error, and the duration. On HTTP it also includes the method, path, and `mcp-session-id` when that header is present. The FRED API key is not logged. Stderr is used so stdio transport keeps its protocol frames on stdout.

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

## Development

```bash
python3.13 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
make check
```

## License

MIT
