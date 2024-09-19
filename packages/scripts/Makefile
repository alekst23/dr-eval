dataset-path ?=

# Define the path to the virtual environment
VENV := ../../venv

# Define the command to activate the virtual environment
ACTIVATE_VENV := . $(shell pwd)/$(VENV)/bin/activate

# Define the root directory of the project
PROJECT_ROOT := $(shell pwd)

setup-env:
	@python -m venv $(VENV)

setup:
	@$(ACTIVATE_VENV) && python3 -m pip install -r requirements.txt

install:
	@$(ACTIVATE_VENV) && python3 -m pip install -e .

reinstall:
	@$(ACTIVATE_VENV) && python3 -m pip uninstall eval_scripts
	@$(ACTIVATE_VENV) && python3 -m pip install -e .

check-install:
	@python -c "import eval_scripts"