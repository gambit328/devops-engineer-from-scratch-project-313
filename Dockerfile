FROM python:3.11-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY . ./
RUN uv sync --frozen --no-dev

CMD [ "uv", "run", "flask", "--app", "main", "run", "--host", "0.0.0.0", "--port", "8080" ]

