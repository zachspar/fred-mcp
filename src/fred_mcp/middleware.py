from __future__ import annotations

import time
from typing import Any

import mcp.types as mt
import structlog
from fastmcp.server.dependencies import get_http_request
from fastmcp.server.middleware import CallNext, Middleware, MiddlewareContext
from fastmcp.tools.base import ToolResult

from fred_mcp.logging import payload_fields

_REQUEST_HEADERS = (("mcp-session-id", "mcp_session_id"),)


def request_fields() -> dict[str, str]:
    """Allowlisted HTTP context. The FRED API key header is not included."""
    try:
        request = get_http_request()
    except RuntimeError:
        return {}

    fields: dict[str, str] = {}
    for header, key in _REQUEST_HEADERS:
        value = request.headers.get(header)
        if value:
            fields[key] = value
    if request.method:
        fields["http_method"] = request.method
    path = request.url.path
    if path:
        fields["http_path"] = path
    return fields


def _arguments(message: Any) -> dict[str, Any]:
    arguments = getattr(message, "arguments", None)
    if arguments is None:
        return {}
    if isinstance(arguments, dict):
        return arguments
    if hasattr(arguments, "model_dump"):
        dumped = arguments.model_dump()
        if isinstance(dumped, dict):
            return dumped
    return {"value": arguments}


def tool_output(result: Any) -> Any:
    structured = getattr(result, "structured_content", None)
    if isinstance(structured, dict):
        return structured
    content = getattr(result, "content", None)
    if isinstance(content, list):
        texts = [
            block.text
            for block in content
            if getattr(block, "text", None) is not None
        ]
        if len(texts) == 1:
            return {"text": texts[0]}
        if texts:
            return {"text": texts}
    return {"repr": repr(result)}


def _emit(level: str, **fields: Any) -> None:
    log = structlog.get_logger("fred_mcp.tools")
    getattr(log, level)("tool_call", **fields)


class ToolCallLoggingMiddleware(Middleware):
    """Log one structlog event per MCP tool call, including both payloads."""

    async def on_call_tool(
        self,
        context: MiddlewareContext[mt.CallToolRequestParams],
        call_next: CallNext[mt.CallToolRequestParams, ToolResult],
    ) -> ToolResult:
        tool_name = getattr(context.message, "name", None) or "unknown"
        arguments = _arguments(context.message)
        started = time.perf_counter()
        try:
            result = await call_next(context)
        except Exception as exc:
            _emit(
                "error",
                tool=tool_name,
                ok=False,
                error=str(exc),
                error_type=type(exc).__name__,
                duration_ms=_duration_ms(started),
                **payload_fields("arguments", arguments),
                **request_fields(),
            )
            raise
        _emit(
            "info",
            tool=tool_name,
            ok=True,
            duration_ms=_duration_ms(started),
            **payload_fields("arguments", arguments),
            **payload_fields("result", tool_output(result)),
            **request_fields(),
        )
        return result


def _duration_ms(started: float) -> float:
    return round((time.perf_counter() - started) * 1000, 2)
