UV := uv
PYTHON := python
FLY_IN := simulation
DEBUGGER := pdb

run: install
	@ $(UV) run $(PYTHON) -m $(FLY_IN)

install:
	@ $(UV) sync

debug:
	@ $(UV) run $(PYTHON) -m $(DEBUGGER) -m $(FLY_IN)

clean:
	@ find . -type d -name "__pycache__" -exec rm -rf {} +
	@ find . -type d -name ".mypy_cache" -exec rm -rf {} +

fclean:
	@ find . -type d -name ".venv" -exec rm -rf {} +

lint:
	@ flake8 . --exclude=.venv && mypy . --exclude=.venv \
	--warn-return-any --warn-unused-ignores \
	--ignore-missing-imports --disallow-untyped-defs \
	--check-untyped-defs

lint-strict:
	@ flake8 . --exclude=.venv && mypy --strict . --exclude=.venv