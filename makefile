# Makefile

.PHONY: lint format

# Run Ruff linter
lint:
	ruff check

# Run Black formatter
format:
	black .

# Run both linting and formatting
all: lint format