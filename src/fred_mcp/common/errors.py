from __future__ import annotations

from fastmcp.exceptions import ToolError
from fred import BaseFredAPIError


def raise_fred_tool_error(error: BaseFredAPIError) -> None:
    message = str(error).strip() or error.__class__.__name__
    raise ToolError(f"FRED API error: {message}") from error
