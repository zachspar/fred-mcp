# Federal Reserve Economic Data MCP Server

> [!NOTE]
> This open-source project is not affiliated with, sponsored by, or endorsed by the *Federal Reserve* or the *Federal Reserve Bank of St. Louis*. "FRED" is a registered trademark of the *Federal Reserve Bank of St. Louis*, used here for descriptive purposes only.

A fully-featured Model Context Protocol (`MCP`) server for accessing Federal Reserve Economic Data ([FRED®](https://fred.stlouisfed.org/)) financial datasets.

This MCP server uses [fred-py-api](https://github.com/zachspar/fred-py-api) under the hood.

## Installation

```bash
pip install fred-mcp
```

## Integration

Easily use this MCP Server in a desktop client of your choosing.

### Recommended

#### [5ire](https://5ire.app/)

See below for an example configuration.

```json
{
  "name": "FRED MCP Server",
  "description": "Get FRED data via MCP",
  "command": "/path/to/fred-mcp",
  "env": {
    "FRED_API_KEY": "<your api key>"
  },
  "isActive": true,
  "key": "FredMcpServer",
  "type": "local"
}
```

#### [Claude Desktop](https://claude.ai/download)

See below for an example configuration.

```json
{
  "mcpServers": {
    "FRED MCP Server": {
      "command": "/path/to/fred-mcp",
      "env": {
        "FRED_API_KEY": "<your api key>"
      }
    }
  }
}
```


## Run Server

### Command-Line

```bash
export FRED_API_KEY=your_api_key
fred-mcp
```

### Docker

```bash
docker run -d -p 8000:8000 -e FRED_API_KEY=your_api_key --name fred-mcp-server ghcr.io/zachspar/fred-mcp/fred-mcp-server:latest
```
