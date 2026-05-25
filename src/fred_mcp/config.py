from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Literal

Transport = Literal["stdio", "sse", "streamable-http"]


@dataclass(frozen=True, slots=True)
class Settings:
    fred_api_key: str | None
    fred_api_key_header: str
    transport: Transport
    host: str
    port: int

    @classmethod
    def from_env(cls) -> Settings:
        port_raw = os.environ.get("MCP_SERVER_PORT", "8000")
        if not port_raw.isnumeric():
            raise ValueError(f"Invalid port number: {port_raw}")

        transport = os.environ.get("MCP_SERVER_TRANSPORT", "stdio")
        if transport not in ("stdio", "sse", "streamable-http"):
            raise ValueError(
                "MCP_SERVER_TRANSPORT must be stdio, sse, or streamable-http"
            )

        return cls(
            fred_api_key=os.environ.get("FRED_API_KEY"),
            fred_api_key_header=os.environ.get(
                "FRED_API_KEY_HEADER", "X-FRED-API-Key"
            ),
            transport=transport,  # type: ignore[arg-type]
            host=os.environ.get("MCP_SERVER_HOST", "localhost"),
            port=int(port_raw),
        )

    def validate_for_transport(self) -> None:
        if self.transport == "stdio" and not self.fred_api_key:
            raise ValueError(
                "FRED_API_KEY is required for stdio transport. "
                "Get a key at https://fredaccount.stlouisfed.org/apikey"
            )


_settings: Settings | None = None


def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings.from_env()
    return _settings


def reset_settings() -> None:
    global _settings
    _settings = None
