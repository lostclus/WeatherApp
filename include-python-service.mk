PYTHON = python3.12
TESTS = tests
PYTEST_OPTS =
VENV_BIN = venv/bin
VENV_LINT_BIN = venv.lint/bin

venv: requirements.txt
	rm -rf $@
	$(PYTHON) -m venv $@
	$(VENV_BIN)/pip install -r $<

venv.lint: requirements.txt requirements.lint.txt
	rm -rf $@
	$(PYTHON) -m venv $@
	$(VENV_LINT_BIN)/pip install -r requirements.txt
	$(VENV_LINT_BIN)/pip install -r requirements.lint.txt

.PHONY: update-requirements
update-requirements: packages.txt requirements.internal.txt
	rm -rf venv
	$(PYTHON) -m venv venv
	$(VENV_BIN)/pip install -r packages.txt -r requirements.internal.txt
	$(VENV_BIN)/pip freeze --exclude-editable > requirements.txt
	cat requirements.internal.txt >> requirements.txt
	touch venv

.PHONY: lint-black
lint-black: venv.lint
	$(VENV_LINT_BIN)/black --check --diff $(PACKAGE) $(TESTS)

.PHONY: lint-ruff
lint-ruff: venv.lint
	$(VENV_LINT_BIN)/ruff check $(PACKAGE) $(TESTS)

.PHONY: lint-mypy
lint-mypy: venv.lint
	$(VENV_LINT_BIN)/mypy $(PACKAGE)

.PHONY: lint
lint: lint-black lint-ruff lint-mypy

.PHONY: ruff-fix
ruff-fix: venv.lint
	$(VENV_LINT_BIN)/ruff --fix $(PACKAGE) $(TESTS)

.PHONY: black-fix
black-fix: venv.lint
	$(VENV_LINT_BIN)/black $(PACKAGE) $(TESTS)

.PHONY: test
test: venv
	$(VENV_BIN)/pytest $(PYTEST_OPTS) $(TESTS)

.PHONY: run
run: venv
	$(VENV_BIN)/python manage.py runserver

.PHONY: clean
clean:
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]' `
	rm -f `find . -type f -name '*~' `
	rm -f `find . -type f -name '.*~' `
	rm -f `find . -type f -name '@*' `
	rm -f `find . -type f -name '#*#' `
	rm -f `find . -type f -name '*.orig' `
	rm -f `find . -type f -name '*.rej' `
	rm -f `find . -type f -name '*.egg-info' `
	rm -rf coverage
	rm -rf cover
	rm -rf htmlcov
	rm -rf .cache
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .eggs
	rm -rf *.egg-info
	rm -rf venv
	rm -rf venv.lint
