from __future__ import annotations

import json
import logging
import os
import sys
from typing import Any

import structlog

_SECRET_KEYS = {
    "api-key",
    "apikey",
    "authorization",
    "password",
    "x-fred-api-key",
}
_REDACTED = "[redacted]"
_DEFAULT_MAX_BODY = 65536


def configure_logging() -> None:
    """JSON logs on stderr so stdio MCP frames stay on stdout."""
    level_name = os.environ.get("MCP_LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            structlog.processors.JSONRenderer(sort_keys=True),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(level),
        logger_factory=structlog.PrintLoggerFactory(file=sys.stderr),
        cache_logger_on_first_use=False,
    )


def max_body_chars() -> int | None:
    raw = os.environ.get("MCP_LOG_MAX_BODY", str(_DEFAULT_MAX_BODY)).strip()
    lowered = raw.lower()
    if lowered in {"0", "none", "unlimited"}:
        return None
    if raw.isnumeric():
        return int(raw)
    return _DEFAULT_MAX_BODY


def _is_secret_key(key: str) -> bool:
    normalized = key.lower().replace("_", "-")
    return normalized in _SECRET_KEYS or normalized.endswith("-api-key")


def redact(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: _REDACTED if _is_secret_key(str(key)) else redact(item)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [redact(item) for item in value]
    return value


def payload_fields(name: str, value: Any) -> dict[str, Any]:
    """Return log fields for a payload, clipping when over the body cap."""
    try:
        encoded = json.dumps(
            redact(value),
            default=str,
            separators=(",", ":"),
            sort_keys=True,
            allow_nan=False,
        )
    except (TypeError, ValueError):
        encoded = json.dumps(
            {"repr": repr(value)},
            separators=(",", ":"),
        )
    size = len(encoded.encode("utf-8"))
    limit = max_body_chars()
    if limit is not None and size > limit:
        return {
            f"{name}_truncated": True,
            f"{name}_bytes": size,
            f"{name}_preview": encoded[:limit],
        }
    return {name: json.loads(encoded), f"{name}_bytes": size}
