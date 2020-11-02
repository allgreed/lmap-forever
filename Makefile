.DEFAULT_GOAL := help
SOURCES_DIR := src
PWD = $(shell pwd)
STORAGE := memory
VARS := ""

# Porcelain
# ###############
.PHONY: container run build lint test

run: setup ## run the app
	PYTHONPATH=$(PWD)/$(SOURCES_DIR) STORAGE_PROVIDER_TYPE=$(STORAGE) $(VARS) uvicorn src.main:app --reload --port 12694

build: setup ## create artifact
	nix build

lint: setup ## run static analysis
	@echo "Not implemented"; false

test: setup ## run all tests
	@echo "Not implemented"; false

container: build ## create container
	nix build -f docker.nix
	mv result docker-image.tar.gz

# Plumbing
# ###############
.PHONY: setup

setup:

# Helpers
# ###############
.PHONY:

# Utilities
# ###############
.PHONY: help todo clean init
init: ## one time setup
	direnv allow .

todo: ## list all TODOs in the project
	git grep -I --line-number TODO | grep -v 'list all TODOs in the project' | grep TODO

clean: ## remove artifacts
	@# will remove everything in .gitignore expect for blocks starting with dep* or lib* comment
	@# TODO: add actual removal xD
	diff --new-line-format="" --unchanged-line-format="" <(grep -v '^#' testowy | grep '\S' | sort) <(awk '/^# *(dep|lib)/,/^$/' testowy | head -n -1 | tail -n +2 | sort) 

help: ## print this message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
