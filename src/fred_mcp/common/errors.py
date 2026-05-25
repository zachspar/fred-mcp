from __future__ import annotations

from fred import BaseFredAPIError
from fastmcp.exceptions import ToolError


def raise_fred_tool_error(error: BaseFredAPIError) -> None:
    message = str(error).strip() or error.__class__.__name__
    raise ToolError(f"FRED API error: {message}") from error
