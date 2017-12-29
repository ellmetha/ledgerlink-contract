.PHONY: qa lint lint_python isort isort_python


# DEVELOPMENT
# ~~~~~~~~~~~
# The following rules can be used during development in order to compile the smart contract and test
# its behavior.
# --------------------------------------------------------------------------------------------------

avm:
	mkdir -p build
	pipenv run python compile.py ledgerlink.py

# QUALITY ASSURANCE
# ~~~~~~~~~~~~~~~~~
# The following rules can be used to check code quality, import sorting, etc.
# --------------------------------------------------------------------------------------------------

qa: lint isort

# Code quality checks (eg. flake8, etc).
lint: lint_python
lint_python:
	pipenv run flake8

# Import sort checks.
isort: isort_python
isort_python:
	pipenv run isort --check-only --recursive --diff .


# TESTING
# ~~~~~~~
# The following rules can be used to trigger tests execution and produce coverage reports.
# --------------------------------------------------------------------------------------------------
