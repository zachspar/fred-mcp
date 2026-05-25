# AGENTS.md

## Cursor Cloud specific instructions

### Overview

A Python MCP server (v1.0.0) for FRED economic data built on FastMCP 3.x. Exposes **31 tools** across five domains (series, categories, releases, sources, tags) via `fastmcp` wrapping `fred-py-api`. Single-service project with no databases or external infrastructure beyond the FRED API.

### Required secrets

- `FRED_API_KEY` — 32-character API key from <https://fredaccount.stlouisfed.org/apikey>. Required for stdio transport; optional for HTTP transports (clients can send via `X-FRED-API-Key` header instead).

### Running the server

```bash
# streamable-http mode (preferred for testing, default in Docker)
FRED_API_KEY=$FRED_API_KEY MCP_SERVER_TRANSPORT=streamable-http MCP_SERVER_PORT=8000 MCP_SERVER_HOST=0.0.0.0 fred-mcp

# stdio mode (default, for MCP client integration)
FRED_API_KEY=$FRED_API_KEY fred-mcp
```

The streamable-http endpoint is at `http://localhost:8000/mcp`.

### Linting and testing

Per the README `Development` section:

```bash
ruff check src tests
pytest
```

### Dependency compatibility

When installing, `fastmcp-slim` (a dependency of `fastmcp`) must install its source `.py` files alongside `.pyc` files. If `from fastmcp.exceptions import ToolError` fails with `ModuleNotFoundError`, run:

```bash
pip install --force-reinstall fastmcp-slim fastmcp
```

This resolves a packaging race condition where `.py` source files are missing from the `fastmcp/` namespace directory.

### Project layout

```
src/fred_mcp/
  main.py              — Entry point, mounts sub-servers, transport config
  config.py            — Settings dataclass, env var parsing
  credentials.py       — API key resolution (env var or HTTP header)
  series/tools.py      — 10 series tools
  categories/tools.py  — 6 category tools
  releases/tools.py    — 9 release tools
  sources/tools.py     — 3 source tools
  tags/tools.py        — 3 tag tools
  common/tools.py      — Shared call_fred helper
  common/errors.py     — ToolError wrapper
  common/types.py      — TypeAlias definitions for FRED API parameters
tests/
  test_tools.py        — Series tool tests + 31-tool count assertion
  test_credentials.py  — API key resolution and settings tests
  test_modules.py      — Parametrized module delegation tests
pyproject.toml         — Build config, dependencies, ruff/pytest config
Dockerfile             — Alpine-based container image
```
