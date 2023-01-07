REQ_DIR := ./requirements/
REQ_MAIN_FILE := $(REQ_DIR)requirements
REQ_DEV_FILE := $(REQ_DIR)requirements-dev

PIP_COMPILE := pip-compile --allow-unsafe --generate-hashes --reuse-hashes

.PHONY: requirements-general-compile
requirements-general-compile:
	@echo "Compile GENERAL requirements from $(REQ_MAIN_FILE)."
	@ $(PIP_COMPILE) $(REQ_MAIN_FILE).in > $(REQ_MAIN_FILE).txt
	@echo "Compiling of $(REQ_MAIN_FILE) finish successfully."

.PHONY: requirements-dev-compile
requirements-dev-compile:
	@echo "Compile DEV requirements from $(REQ_DEV_FILE)."
	@ $(PIP_COMPILE) $(REQ_DEV_FILE).in > $(REQ_DEV_FILE).txt
	@echo "Compiling of $(REQ_DEV_FILE) finish successfully."

.PHONY: requirements-compile
requirements-compile: requirements-general-compile requirements-dev-compile
