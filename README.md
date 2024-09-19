# DR EVAL
## Benchmarking framework for LLM systems

The purpose of this repo is to provide an open-source framework for running evaluations and benchmarks of LLM and RAG systems.

This repo provides several tools to enable the running of itterative tests on your framework:
- Database server for storing test results
- Abstraction layers for integrating your code into the test framework
- Functions for loading data from datasource, creating Q/A set, and running tests against your platform
- Running customizable evaluations of test results
- Viewing evaluation results

## Dev Roadmap
### v0.1.0 (Current version)
- sqlite server
- Jupyter workbooks for running experiments and viewing results

### v0.2.0
- postgres server with pgvector
- database abstraction
- docker containers

### v0.3.0
- api server for database ops
- front-end

### v0.4.0
- library of benchmark and evaluation functions

## Installation

```shell
python3 -m venv venv
make install
```

## Workflow

### 1. Load and populate Q/A data set
#### - From file
`experiment_files.ipynb`

#### - From huggingface
`experiment_data.ipynb`

### 2. Perform completions
`experiment_test.ipynb`

### 3. Perform evaluation
`experiment_eval.ipynb`

### 4. View the results
`experiment_results.ipynb`