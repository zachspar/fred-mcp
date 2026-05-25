FROM python:3.13-alpine

COPY pyproject.toml /app/
COPY src/ /app/src/

WORKDIR /app

ENV PIP_ROOT_USER_ACTION=ignore
RUN pip install -U pip && pip install .

ENV MCP_SERVER_HOST="0.0.0.0"
ENV MCP_SERVER_PORT="8000"
ENV MCP_SERVER_TRANSPORT="streamable-http"

EXPOSE ${MCP_SERVER_PORT}

CMD ["fred-mcp"]
