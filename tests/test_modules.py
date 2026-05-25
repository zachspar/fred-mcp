from __future__ import annotations

import importlib
from unittest.mock import MagicMock

import pytest

TOOL_MODULES = [
    ("fred_mcp.categories.tools", "get_category", "get_category", {"category_id": 125}),
    ("fred_mcp.releases.tools", "list_releases", "get_releases", {}),
    ("fred_mcp.sources.tools", "list_sources", "get_sources", {}),
    ("fred_mcp.tags.tools", "list_tags", "get_tags", {}),
]


@pytest.fixture
def mock_fred_api(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    mock = MagicMock()
    for method in (
        "get_category",
        "get_releases",
        "get_sources",
        "get_tags",
    ):
        getattr(mock, method).return_value = {"ok": True}
    monkeypatch.setattr(
        "fred_mcp.common.tools.resolve_fred_client",
        lambda headers=None: mock,
    )
    return mock


@pytest.mark.parametrize(
    ("module_name", "tool_name", "fred_method", "kwargs"),
    TOOL_MODULES,
)
def test_module_tools_delegate_to_fred_api(
    module_name: str,
    tool_name: str,
    fred_method: str,
    kwargs: dict,
    mock_fred_api: MagicMock,
) -> None:
    module = importlib.import_module(module_name)
    tool_fn = getattr(module, tool_name)
    tool_fn(**kwargs)
    getattr(mock_fred_api, fred_method).assert_called_once()
