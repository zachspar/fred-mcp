# AGENTS.md

## Cursor Cloud specific instructions

### Overview

This is a Python MCP (Model Context Protocol) server for accessing Federal Reserve Economic Data (FRED). It exposes 10 tools via `fastmcp` that wrap the `fred-py-api` library. Single-service project with no databases or external infrastructure beyond the FRED API.

### Required secrets

- `FRED_API_KEY` — 32-character API key from <https://fred.stlouisfed.org/docs/api/api_key.html>. Must be set before running the server; the `fred-py-api` client validates key length at import time.

### Running the server

```bash
# SSE mode (preferred for testing)
FRED_API_KEY=$FRED_API_KEY MCP_SERVER_TRANSPORT=sse MCP_SERVER_PORT=8000 MCP_SERVER_HOST=0.0.0.0 fred-mcp

# stdio mode (default, for MCP client integration)
FRED_API_KEY=$FRED_API_KEY fred-mcp
```

### Linting

```bash
black --check --target-version py312 src/
```

The repo has pre-existing formatting deviations (extra blank lines) that `black` flags. This is a known upstream style choice.

### Dependency compatibility

The project depends on `fastmcp~=2.3.4`. At the time of writing, `pydantic>=2.12` causes a `TypeError: cannot specify both default and default_factory` crash at import time due to a pydantic/fastmcp incompatibility. Pin `pydantic>=2.11,<2.12` if this surfaces. The update script handles this automatically.

### Testing

No automated test suite exists in the repository. To verify the server works, start it in SSE mode and interact via the MCP JSON-RPC protocol over `/sse` and the session-specific `/messages/` endpoint.

### Project layout

```
src/fred_mcp/
  main.py              — Entry point, FastMCP server setup, transport config
  series/mcp.py        — 10 FRED series tools (search, observations, tags, etc.)
  common/types.py      — TypeAlias definitions for FRED API parameters
pyproject.toml         — Build config, dependencies, black config (line-length=79)
Dockerfile             — Alpine-based container image
```
