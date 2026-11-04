run:
	uv run flask --app main --debug run --port 8080

test:
	uv run pytest

lint:
	uv run ruff check
