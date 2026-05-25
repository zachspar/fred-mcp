from __future__ import annotations

from typing import Any

from fred import BaseFredAPIError
from fastmcp.server.dependencies import get_http_headers

from fred_mcp.common.errors import raise_fred_tool_error
from fred_mcp.config import get_settings
from fred_mcp.credentials import resolve_fred_client

READ_ONLY_ANNOTATIONS = {
    "readOnlyHint": True,
    "openWorldHint": True,
}


def _request_headers() -> dict[str, str]:
    settings = get_settings()
    return get_http_headers(include={settings.fred_api_key_header})


def call_fred(method: str, **kwargs: Any) -> Any:
    cleaned = {key: value for key, value in kwargs.items() if value is not None}
    cleaned["file_type"] = "json"
    fred = resolve_fred_client(_request_headers())
    try:
        return getattr(fred, method)(**cleaned)
    except BaseFredAPIError as error:
        raise_fred_tool_error(error)
        raise AssertionError("unreachable")
