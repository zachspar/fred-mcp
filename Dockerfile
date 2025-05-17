FROM python:3.13-slim

COPY src/fred_mcp /app/fred_mcp
COPY pyproject.toml /app

WORKDIR /app

ENV PIP_ROOT_USER_ACTION=ignore
RUN pip install -U pip && pip install .

ENV MCP_SERVER_HOST="0.0.0.0"
ENV MCP_SERVER_PORT="8000"
ENV MCP_SERVER_TRANSPORT="sse"

EXPOSE ${MCP_SERVER_PORT}

CMD ["fred-mcp"]
