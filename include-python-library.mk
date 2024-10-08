PYTHON = python3.12
SRC = src
TESTS = tests
PYTEST_OPTS =
VENV_BIN = venv/bin
VENV_PRE_COMMIT_BIN = venv.pre-commit/bin
VENV_LINT_BIN = venv.lint/bin

venv: pyproject.toml
	rm -rf $@
	$(PYTHON) -m venv $@
	$(VENV_BIN)/pip install -U pip
	$(VENV_BIN)/pip install -e .\[tests\]

venv.lint: pyproject.toml
	rm -rf $@
	$(PYTHON) -m venv $@
	$(VENV_LINT_BIN)/pip install -U pip
	$(VENV_LINT_BIN)/pip install -e .\[lint\]

.PHONY: lint-black
lint-black: venv.lint
	$(VENV_LINT_BIN)/black --check --diff $(SRC) $(TESTS)

.PHONY: lint-ruff
lint-ruff: venv.lint
	$(VENV_LINT_BIN)/ruff check $(SRC) $(TESTS)

.PHONY: lint-mypy
lint-mypy: venv.lint
	$(VENV_LINT_BIN)/mypy $(SRC)

.PHONY: lint
lint: lint-black lint-ruff lint-mypy

.PHONY: ruff-fix
ruff-fix: venv.lint
	$(VENV_LINT_BIN)/ruff --fix $(SRC) $(TESTS)

test: venv
	$(VENV_BIN)/pytest $(PYTEST_OPTS)
