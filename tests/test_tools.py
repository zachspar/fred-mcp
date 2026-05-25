from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from fastmcp.exceptions import ToolError
from fred import BaseFredAPIError

from fred_mcp.main import mcp
from fred_mcp.series.tools import get_series, search_series


@pytest.fixture
def mock_fred_api(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    mock = MagicMock()
    mock.get_series.return_value = {"seriess": [{"id": "GNPCA"}]}
    mock.get_series_search.return_value = {"seriess": []}
    monkeypatch.setattr(
        "fred_mcp.common.tools.resolve_fred_client",
        lambda headers=None: mock,
    )
    return mock


def test_get_series_calls_fred_api(mock_fred_api: MagicMock) -> None:
    result = get_series(series_id="GNPCA")
    mock_fred_api.get_series.assert_called_once_with(
        series_id="GNPCA",
        file_type="json",
    )
    assert result == {"seriess": [{"id": "GNPCA"}]}


def test_search_series_calls_fred_api(mock_fred_api: MagicMock) -> None:
    search_series(search_text="gdp", limit=5)
    mock_fred_api.get_series_search.assert_called_once_with(
        search_text="gdp",
        search_type="full_text",
        limit=5,
        offset=0,
        sort_order="asc",
        file_type="json",
    )


def test_call_fred_raises_tool_error_on_api_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock = MagicMock()
    mock.get_series.side_effect = BaseFredAPIError("bad request")
    monkeypatch.setattr(
        "fred_mcp.common.tools.resolve_fred_client",
        lambda headers=None: mock,
    )
    with pytest.raises(ToolError, match="FRED API error"):
        get_series(series_id="BAD")


@pytest.mark.asyncio
async def test_server_exposes_31_tools() -> None:
    tools = await mcp.list_tools()
    assert len(tools) == 31
