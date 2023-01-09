# Echo collors.
NC := \033[0m
BLUE := \033[0;34m
GREEN := \033[0;32m

CODE_DIR := ./click_pydantic
REQ_DIR := ./requirements/
REQ_MAIN_FILE := $(REQ_DIR)requirements
REQ_DEV_FILE := $(REQ_DIR)requirements-dev

PIP := pip install
PIP_COMPILE := pip-compile -q --resolver=backtracking --allow-unsafe --generate-hashes --reuse-hashes

.PHONY: upgrade-pip
upgrade-pip:
	@ $(PIP) -q --upgrade pip

.PHONY: upgrade-pip-tools
upgrade-pip-tools:
	@ $(PIP) -q --upgrade pip-tools

 .PHONY: prepare-pip
 prepare-pip: upgrade-pip upgrade-pip-tools

.PHONY: requirements-general-compile
requirements-general-compile:
	@echo "$(BLUE)Compile GENERAL requirements from $(REQ_MAIN_FILE).$(NC)"
	@ $(PIP_COMPILE) $(REQ_MAIN_FILE).in > $(REQ_MAIN_FILE).txt
	@echo "$(GREEN)Compiling of $(REQ_MAIN_FILE) finish successfully.\n$(NC)"

.PHONY: requirements-dev-compile
requirements-dev-compile:
	@echo "$(BLUE)Compile DEV requirements from $(REQ_DEV_FILE).$(NC)"
	@$(PIP_COMPILE) $(REQ_DEV_FILE).in > $(REQ_DEV_FILE).txt
	@echo "$(GREEN)Compiling of $(REQ_DEV_FILE) finish successfully.\n$(NC)"

.PHONY: requirements-compile
requirements-compile: requirements-general-compile requirements-dev-compile

.PHONY: install-general-requirements
install-general-requirements: prepare-pip
	@echo "$(BLUE)Install GENERAL requirements form $(REQ_DEV_FILE).$(NC)"
	@ $(PIP) -q -r $(REQ_MAIN_FILE).txt
	@echo "$(GREEN)Installing of $(REQ_MAIN_FILE) finish successfully.\n$(NC)"

.PHONY: install-dev-requirements
install-dev-requirements: install-general-requirements
	@echo "$(BLUE)Install DEV requirements from $(REQ_DEV_FILE).$(NC)"
	@ $(PIP) -q -r $(REQ_DEV_FILE).txt
	@echo "$(GREEN)Installing of $(REQ_DEV_FILE) finish successfully.\n$(NC)"

.PHONY: linters-check
linters-check:
	@echo "$(BLUE)Start mypy check code.$(NC)"
	@mypy $(CODE_DIR)
	@echo "$(BLUE)Start black check code.$(NC)"
	@black --check --diff --line-length 79 $(CODE_DIR)
	@echo "$(BLUE)Start isort check code.$(NC)"
	@isort --check --diff $(CODE_DIR)
	@echo "$(BLUE)Start flake8 check code.$(NC)"
	@flake8 --max-line-length 79 $(CODE_DIR)
	@echo "$(GREEN)All linters check finished successfully.$(NC)"

.PHONY: linters-format
linters-format:
	@echo "$(BLUE)Start black format code.$(NC)"
	@black $(CODE_DIR)
	@echo "$(BLUE)Start isort format code.$(NC)"
	@isort $(CODE_DIR)
	@echo "$(BLUE)Start flake8 format code.$(NC)"
	@flake8 $(CODE_DIR)
	@echo "$(GREEN)All linters finished formatting code.$(NC)"
