from __future__ import annotations

from fred import FredAPI
from fastmcp.exceptions import ToolError

from fred_mcp.config import get_settings


def _lookup_header(headers: dict[str, str], header_name: str) -> str | None:
    target = header_name.lower()
    for key, value in headers.items():
        if key.lower() == target and value.strip():
            return value.strip()
    return None


def resolve_api_key(headers: dict[str, str] | None = None) -> str:
    settings = get_settings()
    key = _lookup_header(headers or {}, settings.fred_api_key_header)
    if not key:
        key = settings.fred_api_key
    if not key:
        raise ToolError(
            "FRED API key required. For stdio, set the FRED_API_KEY environment "
            f"variable. For HTTP, send the {settings.fred_api_key_header} header."
        )
    return key


def resolve_fred_client(headers: dict[str, str] | None = None) -> FredAPI:
    return FredAPI(resolve_api_key(headers))
