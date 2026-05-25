from __future__ import annotations

import os
from unittest.mock import MagicMock

import pytest
from fastmcp.exceptions import ToolError

from fred_mcp.config import Settings, reset_settings
from fred_mcp.credentials import resolve_api_key, resolve_fred_client


@pytest.fixture(autouse=True)
def clean_settings(monkeypatch: pytest.MonkeyPatch) -> None:
    reset_settings()
    monkeypatch.delenv("FRED_API_KEY", raising=False)
    monkeypatch.delenv("FRED_API_KEY_HEADER", raising=False)
    monkeypatch.delenv("MCP_SERVER_TRANSPORT", raising=False)
    monkeypatch.delenv("MCP_SERVER_HOST", raising=False)
    monkeypatch.delenv("MCP_SERVER_PORT", raising=False)


@pytest.fixture
def mock_fred_api(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    mock = MagicMock()
    mock.get_series.return_value = {"seriess": []}
    monkeypatch.setattr("fred_mcp.common.tools.resolve_fred_client", lambda headers=None: mock)
    return mock


@pytest.fixture
def api_key_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FRED_API_KEY", "a" * 32)


def test_resolve_api_key_from_header() -> None:
    os.environ["FRED_API_KEY"] = "b" * 32
    reset_settings()
    assert resolve_api_key({"X-FRED-API-Key": "a" * 32}) == "a" * 32


def test_resolve_api_key_from_env_fallback() -> None:
    os.environ["FRED_API_KEY"] = "c" * 32
    reset_settings()
    assert resolve_api_key({}) == "c" * 32


def test_resolve_api_key_missing_raises_tool_error() -> None:
    reset_settings()
    with pytest.raises(ToolError, match="FRED API key required"):
        resolve_api_key({})


def test_resolve_fred_client_uses_key(monkeypatch: pytest.MonkeyPatch) -> None:
    created: list[str] = []

    class FakeFredAPI:
        def __init__(self, key: str) -> None:
            created.append(key)

    monkeypatch.setattr("fred_mcp.credentials.FredAPI", FakeFredAPI)
    os.environ["FRED_API_KEY"] = "d" * 32
    reset_settings()
    resolve_fred_client()
    assert created == ["d" * 32]


def test_settings_validate_stdio_requires_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MCP_SERVER_TRANSPORT", "stdio")
    reset_settings()
    settings = Settings.from_env()
    with pytest.raises(ValueError, match="FRED_API_KEY is required"):
        settings.validate_for_transport()


def test_settings_validate_http_allows_missing_key(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("MCP_SERVER_TRANSPORT", "streamable-http")
    reset_settings()
    settings = Settings.from_env()
    settings.validate_for_transport()
