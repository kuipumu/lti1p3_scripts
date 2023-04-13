.PHONY: help requirements quality

.DEFAULT_GOAL := help

MODULES = token_request.py

help: ## display this help message
	@echo "Please use \`make <target>' where <target> is one of"
	@awk -F ':.*?## ' '/^[a-zA-Z]/ && NF==2 {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort

requirements: ## install requirements
	pip install -r requirements.txt

quality: ## Check code style
	pylint ${MODULES}
	pycodestyle ${MODULES}
	pydocstyle ${MODULES}
	isort --check-only --diff ${MODULES}
