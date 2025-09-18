PY=python3
VENV=.venv
PIP=$(VENV)/bin/pip
PYBIN=$(VENV)/bin/python

.PHONY: venv install run test docker-build docker-run clean

venv:
	$(PY) -m venv $(VENV)
	@echo "Created virtualenv in $(VENV). Activate with: source $(VENV)/bin/activate"

install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run: install
	$(PYBIN) -m app.main

test: install
	$(PYBIN) -m pytest -q

docker-build:
	docker build -t anythingllm-app:latest .

docker-run: docker-build
	docker run --rm -p 8000:8000 anythingllm-app:latest

clean:
	rm -rf $(VENV) .pytest_cache
