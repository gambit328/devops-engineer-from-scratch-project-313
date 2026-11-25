FROM node:22-slim AS frontend
WORKDIR /front
COPY package*.json ./
RUN npm ci

FROM python:3.11-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app
COPY . ./
COPY --from=frontend /front/node_modules/@hexlet/project-devops-deploy-crud-frontend/dist/ ./public/
RUN uv sync --frozen --no-dev

CMD [ "uv", "run", "flask", "--app", "main", "run", "--host", "0.0.0.0", "--port", "8080" ]

