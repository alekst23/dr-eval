# Define the path to the virtual environment
VENV := ../../venv

# Define the command to activate the virtual environment
ACTIVATE_VENV := . $(shell pwd)/$(VENV)/bin/activate

install:
	@$(ACTIVATE_VENV) && python3 -m pip install -e .

reinstall:
	@$(ACTIVATE_VENV) && python3 -m pip uninstall eval_data
	@$(ACTIVATE_VENV) && python3 -m pip install -e .

check-install:
	@python -c "import eval_data"