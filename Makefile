setup:
	uv sync --locked
data:
	uv run crb fetch
all:
	uv run crb run
	uv run crb publish
test:
	uv run ruff check .
	uv run ruff format --check .
	uv run pytest
