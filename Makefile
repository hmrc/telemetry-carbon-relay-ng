SHELL := /usr/bin/env bash
POETRY_OK := $(shell type -P poetry)
POETRY_PATH := $(shell poetry env info --path)
POETRY_REQUIRED := $(shell cat .poetry-version)
POETRY_VIRTUALENVS_IN_PROJECT ?= true
PYTHON_OK := $(shell type -P python)
PYTHON_REQUIRED := $(shell cat .python-version)
PYTHON_VERSION ?= $(shell python -V | cut -d' ' -f2)

### WARNING! This is a generated file and should ONLY be edited in https://github.com/hmrc/telemetry-docker-resources

help: ## The help text you're reading
	@grep --no-filename -E '^[a-zA-Z1-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.PHONY: help



check_poetry: check_python ## Check Poetry installation
    ifeq ('$(POETRY_OK)','')
	    $(error package 'poetry' not found!)
    else
	    @echo Found Poetry ${POETRY_REQUIRED}
    endif
.PHONY: check_poetry

check_python: ## Check Python installation
    ifeq ('$(PYTHON_OK)','')
	    $(error python interpreter: 'python' not found!)
    else
	    @echo Found Python
    endif
    ifneq ('$(PYTHON_REQUIRED)','$(PYTHON_VERSION)')
	    $(error incorrect version of python found: '${PYTHON_VERSION}'. Expected '${PYTHON_REQUIRED}'!)
    else
	    @echo Found Python ${PYTHON_REQUIRED}
    endif
.PHONY: check_python

clean: ## Teardown build artefacts
	@sudo rm -rf ./build ./venv ./venv_package
.PHONY: clean

cruft_update: ## Update cruft but saving the current state of the complex input variables
	@cp .cruft.json ~/.cruft.json.bak
	@cruft update --variables-to-update-file ~/.cruft.json.bak
	@rm ~/.cruft.json.bak
.PHONY: clean

cut_release: ## Cut release
	@./bin/docker-tools.sh cut_release
.PHONY: cut_release

debug_env: ## Print out variables used by docker-tools.sh
	@./bin/docker-tools.sh debug_env
.PHONY: debug_env

prepare_release: ## Runs prepare release
	@./bin/docker-tools.sh prepare_release
.PHONY: prepare_release

publish_to_ecr: ## Push the Docker image to the internal-base ECR repo
	@./bin/docker-tools.sh publish_to_ecr
.PHONY: publish_to_ecr

setup: check_poetry ## Setup virtualenv & dependencies using poetry and set-up the git hook scripts
	@export POETRY_VIRTUALENVS_IN_PROJECT=$(POETRY_VIRTUALENVS_IN_PROJECT) && poetry run pip install --upgrade pip
	@poetry config --list
	@poetry install --no-root
	@poetry run pre-commit install
.PHONY: setup

verify: setup prepare_release ## Build the Docker image
	@./bin/docker-tools.sh package
.PHONY: verify

verify_publish_release: verify publish_to_ecr cut_release ## Build Docker image with appropriate tags, publish and push new tag to GitHub
.PHONY: verify_publish_release
