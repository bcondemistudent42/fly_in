SRC = src
RUN = uv run python3 -m

install: .venv/uv.lock

debug: install
	@echo "Debug mode: "
	$(PYTHON) -m pdb src/__main__.py


.venv/uv.lock: pyproject.toml
	@echo "Installing dependencies using uv..."
	uv sync
	@touch .venv/uv.lock

run:
	$(RUN) $(SRC)

clean:
	find src -name "*pyc*" -type d -exec rm -rf {} +