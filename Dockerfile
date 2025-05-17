FROM python:3.13-slim

COPY src/fred_mcp /app/fred_mcp
COPY pyproject.toml /app

WORKDIR /app

ENV PIP_ROOT_USER_ACTION=ignore
RUN pip install -U pip && pip install .

EXPOSE 8000
CMD ["fred-mcp"]
