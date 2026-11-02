from __future__ import annotations

import json
import logging
import os
import re
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


def max_body_bytes() -> int | None:
    """Byte cap for one logged payload. None means do not clip.

    ``MCP_LOG_MAX_BODY=0`` (also ``none`` or ``unlimited``) disables the
    cap. Any other non-numeric value falls back to 65536.
    """
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
    """Replace values of secret field names. Does not scan string contents.

    Walks dicts, lists, and tuples. A secret name is ``api_key``,
    ``authorization``, ``password``, or a name ending in ``api-key``.
    """
    if isinstance(value, dict):
        return {
            key: _REDACTED if _is_secret_key(str(key)) else redact(item)
            for key, item in value.items()
        }
    if isinstance(value, (list, tuple)):
        return [redact(item) for item in value]
    return value


def scrub_secrets(text: str) -> str:
    """Blank values assigned to secret names, such as ``api_key=...``."""
    names = ["api[_-]?key", "authorization", "password"]
    header = os.environ.get("FRED_API_KEY_HEADER")
    if header:
        names.append(re.escape(header))
    pattern = re.compile(
        rf"(?i)({'|'.join(names)})(\s*[:=]\s*)[^&\s\"']+"
    )
    return pattern.sub(
        lambda match: f"{match.group(1)}{match.group(2)}{_REDACTED}",
        text,
    )


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
            {"repr": repr(redact(value))},
            separators=(",", ":"),
        )
    raw = encoded.encode("utf-8")
    size = len(raw)
    limit = max_body_bytes()
    if limit is not None and size > limit:
        return {
            f"{name}_truncated": True,
            f"{name}_bytes": size,
            f"{name}_preview": raw[:limit].decode("utf-8", errors="ignore"),
        }
    return {name: json.loads(encoded), f"{name}_bytes": size}
