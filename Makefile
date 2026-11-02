.DEFAULT_GOAL := check

.PHONY: check lint test

check: lint test

lint:
	ruff check src tests

test:
	pytest
