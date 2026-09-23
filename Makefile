UV := $(shell command -v uv 2>/dev/null || echo "$(HOME)/.local/bin/uv")
PYTHON := python

# Cross - platform defaults (used on machine with and without goinfre)
VENV := .venv
UV_CACHE_DIR := $(shell uv cache dir 2>/dev/null || echo "$(HOME)/.cache/uv")
HF_HOME := $(HOME)/.cache/huggingface

# Override with goinfre paths on 42 campus machines
ifneq ($(wildcard /goinfre/.),)
VENV := /goinfre/$(USER)/call-me-maybe-venv
UV_CACHE_DIR := /goinfre/$(USER)/uv-cache
HF_HOME := /goinfre/$(USER)/hf-cache
endif

export UV_CACHE_DIR
export HF_HOME
export UV_PROJECT_ENVIRONMENT := $(VENV)

FUNCTIONS_DEFINITIONS ?= data/input/functions_definition.json
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
	mkdir -p "$(UV_CACHE_DIR)" "$(HF_HOME)"
	$(UV) sync
	@echo "Virtual environment ready: $(VENV)"
	@echo "Run: source $(VENV)/bin/activate";

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

purge: fclean
	rm -rf "$(UV_CACHE_DIR)"
	rm -rf "$(HF_HOME)"

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