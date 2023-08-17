.PHONY: help upgrade requirements dev-requirements quality

.DEFAULT_GOAL := help

PIP_COMPILE = pip-compile --upgrade

MODULES = token_request.py

help: ## display this help message
	@echo "Please use \`make <target>' where <target> is one of"
	@awk -F ':.*?## ' '/^[a-zA-Z]/ && NF==2 {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort

upgrade: ## update the requirements/*.txt files with the latest packages satisfying requirements/*.in
	pip install -qr requirements/pip-tools.txt
	# Make sure to compile files after any other files they include!
	$(PIP_COMPILE) --allow-unsafe -o requirements/pip-tools.txt requirements/pip-tools.in
	$(PIP_COMPILE) -o requirements/base.txt requirements/base.in
	$(PIP_COMPILE) -o requirements/quality.txt requirements/quality.in

requirements: ## install requirements
	pip install -r requirements/base.txt

dev-requirements: requirements ## install development requirements
	pip install -r requirements/quality.txt

quality: ## Check code style
	pylint ${MODULES}
	pycodestyle ${MODULES}
	pydocstyle ${MODULES}
	isort --check-only --diff ${MODULES}
