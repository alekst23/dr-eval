# Define the path to the virtual environment
VENV := venv

# Define the root directory of the project
PROJECT_ROOT := $(shell pwd)

run-sample-dataset:
	cd src/eval-scripts && make sample-dataset dataset-path="$(PROJECT_ROOT)/datasets/fin"

setup:
	pip install setuptools
	pip install -r requirements.txt


install-data:
	cd packages/data && make install

install-scripts:
	cd packages/scripts && make install

install-serv:
	cd packages/serv && make install

install: install-data install-scripts

reinstall:
	pip uninstall dreval
	pip install -e .
	
all: setup install