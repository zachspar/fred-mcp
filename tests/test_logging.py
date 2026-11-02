from __future__ import annotations

import json
from unittest.mock import MagicMock

import pytest
import structlog
from fastmcp.exceptions import ToolError
from fred import BaseFredAPIError
from starlette.requests import Request
from structlog.testing import capture_logs

from fred_mcp.logging import configure_logging, payload_fields, redact
from fred_mcp.main import mcp
from fred_mcp.middleware import ToolCallLoggingMiddleware, request_fields
from fred_mcp.series.tools import get_series


def _http_request() -> Request:
    return Request(
        {
            "type": "http",
            "http_version": "1.1",
            "method": "POST",
            "scheme": "https",
            "path": "/mcp",
            "raw_path": b"/mcp",
            "query_string": b"",
            "headers": [
                (b"fly-region", b"iad"),
                (b"fly-client-ip", b"203.0.113.8"),
                (b"fly-request-id", b"req-1"),
                (b"mcp-session-id", b"sess-1"),
                (b"x-fred-api-key", b"super-secret-key"),
            ],
            "client": ("203.0.113.8", 443),
            "server": ("10.0.0.1", 8000),
        }
    )


@pytest.fixture
def mock_fred_api(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    mock = MagicMock()
    mock.get_series.return_value = {"seriess": [{"id": "GNPCA"}]}
    monkeypatch.setattr(
        "fred_mcp.common.tools.resolve_fred_client",
        lambda headers=None: mock,
    )
    return mock


def test_redact_hides_api_key_fields() -> None:
    cleaned = redact(
        {
            "series_id": "GNPCA",
            "api_key": "abc",
            "nested": [{"X-FRED-API-Key": "xyz"}],
        }
    )
    assert cleaned == {
        "series_id": "GNPCA",
        "api_key": "[redacted]",
        "nested": [{"X-FRED-API-Key": "[redacted]"}],
    }


def test_payload_fields_truncate(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MCP_LOG_MAX_BODY", "32")
    fields = payload_fields("result", {"observations": ["x" * 80]})
    assert fields["result_truncated"] is True
    assert fields["result_bytes"] > 32
    assert len(fields["result_preview"]) == 32
    assert "result" not in fields


def test_request_fields_empty_without_http(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def _missing() -> Request:
        raise RuntimeError("No active HTTP request found.")

    monkeypatch.setattr("fred_mcp.middleware.get_http_request", _missing)
    assert request_fields() == {}


def test_request_fields_keep_client_context_and_drop_api_key(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "fred_mcp.middleware.get_http_request",
        _http_request,
    )
    fields = request_fields()
    assert fields == {
        "mcp_session_id": "sess-1",
        "http_method": "POST",
        "http_path": "/mcp",
    }
    assert "iad" not in fields.values()
    assert "super-secret-key" not in fields.values()


def test_tool_logging_middleware_is_registered() -> None:
    assert any(
        isinstance(item, ToolCallLoggingMiddleware) for item in mcp.middleware
    )


def test_direct_tool_call_is_not_logged(mock_fred_api: MagicMock) -> None:
    with capture_logs() as logs:
        get_series(series_id="GNPCA")
    assert logs == []
    mock_fred_api.get_series.assert_called_once()


@pytest.mark.asyncio
async def test_tool_call_logs_arguments_result_and_request(
    mock_fred_api: MagicMock,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "fred_mcp.middleware.get_http_request",
        _http_request,
    )
    with capture_logs() as logs:
        await mcp.call_tool("get_series", {"series_id": "GNPCA"})

    events = [entry for entry in logs if entry.get("event") == "tool_call"]
    assert len(events) == 1
    event = events[0]
    assert event["tool"] == "get_series"
    assert event["ok"] is True
    assert event["arguments"] == {"series_id": "GNPCA"}
    assert event["result"] == {"seriess": [{"id": "GNPCA"}]}
    assert event["mcp_session_id"] == "sess-1"
    assert event["http_method"] == "POST"
    assert event["http_path"] == "/mcp"
    encoded = json.dumps(event)
    assert "super-secret-key" not in encoded
    assert "iad" not in encoded
    assert "203.0.113.8" not in encoded
    assert "req-1" not in encoded
    mock_fred_api.get_series.assert_called_once()


@pytest.mark.asyncio
async def test_tool_call_logs_error_with_arguments(
    mock_fred_api: MagicMock,
) -> None:
    mock_fred_api.get_series.side_effect = BaseFredAPIError("bad request")
    with (
        capture_logs() as logs,
        pytest.raises(ToolError, match="FRED API error"),
    ):
        await mcp.call_tool("get_series", {"series_id": "BAD"})

    events = [entry for entry in logs if entry.get("event") == "tool_call"]
    assert len(events) == 1
    event = events[0]
    assert event["ok"] is False
    assert event["tool"] == "get_series"
    assert event["arguments"] == {"series_id": "BAD"}
    assert event["error_type"] == "ToolError"
    assert "bad request" in event["error"]
    assert "result" not in event


def test_configure_logging_writes_json_to_stderr(
    capsys: pytest.CaptureFixture[str],
) -> None:
    configure_logging()
    structlog.get_logger("fred_mcp").info("server_start", transport="stdio")
    captured = capsys.readouterr()
    assert captured.out == ""
    payload = json.loads(captured.err.strip())
    assert payload["event"] == "server_start"
    assert payload["transport"] == "stdio"
    assert payload["level"] == "info"
