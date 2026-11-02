# AGENTS.md

Open-source MCP server for FRED economic data. FastMCP 3 wraps `fred-py-api`. One process, no database, no cache. Version is in `pyproject.toml`. Python `>=3.10`. CI runs on 3.13.

The server exposes 31 read-only tools in five domains, plus the `fred_research_workflow` prompt. `tests/test_tools.py` asserts the tool count. Change that assertion when you add or remove a tool.

## Setup and checks

```bash
python3.13 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
make check
```

`make check` runs `ruff check src tests` and then `pytest`. `make lint` and `make test` run one of those. CI calls `make check` on pull requests and pushes to `main` when `src/`, `tests/`, `pyproject.toml`, the `Makefile`, the Dockerfile, or the workflow file changes. A published GitHub Release publishes the package to PyPI and the Docker image to GHCR as `latest`, the release git tag, and the released commit SHA. Pushes to `main` do neither. The image runs `fred-mcp` with `MCP_SERVER_TRANSPORT=streamable-http` on `0.0.0.0:8000`.

Run the server:

```bash
# stdio (default). FRED_API_KEY is required.
FRED_API_KEY=$FRED_API_KEY fred-mcp

# HTTP. Clients send their own key. Endpoint: http://localhost:8000/mcp
MCP_SERVER_TRANSPORT=streamable-http MCP_SERVER_HOST=0.0.0.0 MCP_SERVER_PORT=8000 fred-mcp
```

`MCP_SERVER_TRANSPORT` is `stdio`, `streamable-http`, or `sse`.

## Where a change goes

`main.py` builds the server, mounts the five domain servers, and installs `ToolCallLoggingMiddleware`. Add a tool on the domain server in `src/fred_mcp/<domain>/tools.py`. Mount a new domain from `main.py`.

Each tool is a thin function:

- Decorate with `@<domain>_mcp.tool`. Set `name` (snake_case), a description that includes an example call, and `annotations={**READ_ONLY_ANNOTATIONS, "title": "..."}`.
- Accept FRED parameters explicitly. Use the `Literal` aliases in `common/types.py` for enums. Add a new alias there instead of inlining a new set of allowed strings.
- Return `call_fred("<fred-py-api method>", ...)`. `call_fred` drops `None` values and sets `file_type="json"`. Do not pass the API key in. Do not call `FredAPI` from a tool.
- Let FRED failures raise `ToolError` through `raise_fred_tool_error`. Do not return `{"error": ...}`.

Only wrap methods `fred-py-api` already exposes. Keep the tool name and the FRED method name distinct when they differ (`search_series` calls `get_series_search`).

## Credentials

`resolve_api_key` prefers the HTTP header (`X-FRED-API-Key`, or `FRED_API_KEY_HEADER`) and falls back to `FRED_API_KEY`. Stdio has no header, so the environment variable is required there. HTTP can run with no server-side key so each client brings its own.

`get_settings()` caches the first read of the environment. Tests that change env vars call `reset_settings()`.

Never log the API key, the header that carries it, or any value under an `api_key` / `authorization` / `password` field. `redact()` scrubs those fields in tool payloads. `scrub_secrets()` blanks `name=value` secrets in error text, including a FRED `api_key` query parameter. Do not log raw request headers.

## Logging

`configure_logging()` in `main()` writes structlog JSON to stderr. Stdout must stay free for stdio MCP frames.

`ToolCallLoggingMiddleware` emits one `tool_call` event per MCP tool call: tool name, arguments, result or error, and duration. On HTTP it also records the method, path, and `mcp-session-id` when the client sends that header. It does not record host-specific headers.

`MCP_LOG_LEVEL` defaults to `INFO`. `MCP_LOG_MAX_BODY` defaults to `65536` bytes of arguments or result per line. `0` keeps the full payload. Cover a logging change with `tests/test_logging.py`.

## Tests

Tests must not call the FRED API. Patch `fred_mcp.common.tools.resolve_fred_client` and assert the method name and kwargs the tool forwarded.

- `test_tools.py` covers series tools and the tool count.
- `test_modules.py` checks one delegated call per other domain.
- `test_credentials.py` covers key resolution. It resets settings.
- `test_logging.py` uses `structlog.testing.capture_logs`. A direct call to a tool function does not log. Logging runs only through `mcp.call_tool`.

`asyncio_mode` is `auto`.

## Style

Ruff line length is 79. Target is Python 3.10, so new syntax has to run there. Match the imports and docstring tone of the file you edit. Do not add a dependency unless a tool in this repo needs it.

## Layout

```
src/fred_mcp/
  main.py              Entry point, mounts, logging middleware
  config.py            Env settings
  credentials.py       API key resolution
  logging.py           structlog setup, redaction, payload clipping
  middleware.py        Per-tool-call log line
  common/tools.py      call_fred
  common/errors.py     FRED errors to ToolError
  common/types.py      FRED parameter literals
  series/tools.py      10 tools
  categories/tools.py  6 tools
  releases/tools.py    9 tools
  sources/tools.py     3 tools
  tags/tools.py        3 tools
tests/                 Pytest, no live HTTP
Dockerfile             Python 3.13 Alpine image
```

## Install footgun

`fastmcp` depends on `fastmcp-slim`. A bad install leaves the `fastmcp` namespace without `.py` files, and `from fastmcp.exceptions import ToolError` raises `ModuleNotFoundError`. Fix it with:

```bash
pip install --force-reinstall fastmcp-slim fastmcp
```
