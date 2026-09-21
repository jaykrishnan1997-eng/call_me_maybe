UV := $(shell command -v uv 2>/dev/null || echo "$(HOME)/.local/bin/uv")
VENV := .venv
PYTHON := python

# Use goinfree for caches/venv if it exists, else fall back to defaults
ifneq ($(wildcard /goinfre/.),)
export UV_CACHE_DIR := /goinfre/$(USER)/uv-cache
export HF_HOME := /goinfre/$(USER)/hf-cache
export UV_PROJECT_ENVIRONMENT := /goinfre/$(USER)/call-me-maybe-venv
endif

FUNCTIONS_DEFINITIONS ?= data/input/function_definition.json
INPUT ?= data/input/function_calling_tests.json
OUTPUT ?= data/output/function_calling_result.json

.PHONY: install run debug clean fclean lint lint-strict

install:
	@if [ ! -x "$(UV)" ]; then \
		echo "uv not found. Installing uv..."; \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
	fi
	@if [ ! -x "$(UV)" ]; then \
		echo "Error: uv installation failed."; \
		exit 1; \
	fi
	@if [ -n "$(UV_CACHE_DIR)" ]; then mkdir -p "$(UV_CACHE_DIR)"; fi
	@if [ -n "$(HF_HOME)" ]; then mkdir -p "$(HF_HOME)"; fi
	$(UV) sync
	@echo "Virtual environment ready: $(VENV)"
	@echo "Run: source /goinfre/$USER/call-me-maybe-venv/bin/activate";

run: install
	$(UV) run $(PYTHON) -m src \
		--function_definition $(FUNCTIONS_DEFINITIONS) \
		--input $(INPUT) \
		--output $(OUTPUT)
		
debug: install
	$(UV) run $(PYTHON) -m pdb -m src \
		--function_definition $(FUNCTIONS_DEFINITIONS) \
		--input $(INPUT) \
		--output $(OUTPUT)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -name "*.pyc" -delete

fclean: clean
	rm -rf $(VENV)
	@if [ -n "$(UV_PROJECT_ENVIRONMENT)" ]; then rm -rf "$(UV_PROJECT_ENVIRONMENT)"; fi

purge: fclean
	@if [ -n "$(UV_CACHE_DIR)" ]; then rm -rf "$(UV_CACHE_DIR)"; fi
	@if [ -n "$(HF_HOME)" ]; then rm -rf "$(HF_HOME)"; fi

lint: install
	$(UV) run flake8 . --exclude=.venv,venv,llm_sdk
	$(UV) run mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

lint-strict: install
	$(UV) run flake8 . --exclude=.venv,venv,llm_sdk
	$(UV) run mypy . --strict