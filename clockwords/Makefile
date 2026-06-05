.PHONY: test lint fmt dump-menu

test:
	uv run pytest

lint:
	uv run ruff check src tests
	uv run mypy

fmt:
	uv run ruff format src tests

dump-menu:
	uv run scripts/dump_time_menu.py
