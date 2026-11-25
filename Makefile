.PHONY: dev

run:
	uv run flask --app main --debug run --port 8080

test:
	uv run pytest

lint:
	uv run ruff check

dev:
	npx concurrently \
	"make run" \
	"npx start-hexlet-devops-deploy-crud-frontend"

build:
	uv sync
	npm ci
	mkdir -p public
	cp -r ./node_modules/@hexlet/project-devops-deploy-crud-frontend/dist/. public/
