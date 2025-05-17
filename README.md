# fred-mcp
FRED Python MCP server with fred-py-api

## Installation
```bash
pip install fred-mcp
```

## Run Server
### Command Line
```bash
fred-mcp
```

### Run with Docker
```bash
docker run -d -p 8000:8000 -e FRED_API_KEY=your_api_key --name fred-mcp-server ghcr.io/zachspar/fred-mcp/fred-mcp-server:latest
```