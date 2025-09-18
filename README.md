# Financial Tracking Application

## Purpose
The Financial Tracking Application will be used for tracking simple monthly bills for the rest of the year. The project will expand as it's developed, tested and used.

## Tools

- AnythingLLM
- AnythingLLM VS Code Extension
- VS Code
- Docker
- GitHub Account
- Python 3

## Procedures

## Quick start: store sample scraped data

This repository includes a minimal utility to persist scraped items into a local SQLite database.

Files added for examples:
- `scripts/store_data.py` — CLI script that writes items into `db/items.db` and optionally dumps JSON.
- `data/sample_items.json` — a small sample dataset you can use to test the script.

Run the sample import (use `python3` on macOS):

```bash
# create a virtualenv (optional but recommended)
python3 -m venv .venv
source .venv/bin/activate

# import sample items into the default DB
python3 scripts/store_data.py --json-in data/sample_items.json

# confirm with sqlite3 CLI (if installed):
sqlite3 db/items.db "SELECT pk,id,url,title,scraped_at FROM items LIMIT 5;"
```

If you prefer to inspect the DB in VS Code, see the `.github/copilot-instructions.md` for recommended extensions. Two quick options:

- SQLTools + SQLite driver: `mtxr.sqltools` and `mtxr.sqltools-driver-sqlite` — install via the Extensions view or:

```bash
code --install-extension mtxr.sqltools
code --install-extension mtxr.sqltools-driver-sqlite
```

- SQLite explorer (simple): `alexcvzz.vscode-sqlite`

Sample query you can run in either tool:

```sql
SELECT pk, id, url, title, scraped_at, source
FROM items
ORDER BY scraped_at DESC
LIMIT 20;
```

## Run the FastAPI app (development)

The project includes a minimal FastAPI app under the `app/` package. Start it locally with the provided Makefile or directly with the Python module entrypoint:

```bash
# using the Makefile (recommended for dev tasks)
make run

# or run the module directly
.venv/bin/python -m app.main
```

The API exposes at least these endpoints:

- `GET /health` — health check
- `GET /items` — list scraped items
- `POST /scrape` — run a small stub scraper and persist results (uses the storage utility)

## Running the test suite

Tests use `pytest` and FastAPI's TestClient. Run the tests from the project root after activating your venv:

```bash
.venv/bin/python -m pytest -q
```

Note: the test suite pins a compatible `httpx` version in `requirements.txt`. If you run into TestClient errors, ensure you installed dependencies from `requirements.txt` (see below).

## Dependencies and environment notes

- A `requirements.txt` file is included for quick setup. Install into your virtualenv with:

```bash
.venv/bin/python -m pip install -r requirements.txt
```

- The `httpx` dependency is intentionally pinned for test compatibility with the Starlette/FastAPI test client. If you want to upgrade `httpx`, update `requirements.txt` and run tests locally.

## Docker

There is a `Dockerfile` for building a containerized version of the FastAPI app. The image is a simple dev/proof-of-concept image — consider multi-stage builds and non-root users for production.

Build and run the container locally:

```bash
make docker-build
make docker-run
```

## VS Code DB inspection

To inspect the SQLite DB (`db/items.db`) from VS Code, install one of these extensions:

- SQLTools + SQLite driver: `mtxr.sqltools` and `mtxr.sqltools-driver-sqlite`
- SQLite explorer (lightweight): `alexcvzz.vscode-sqlite`

See the `.github/copilot-instructions.md` for the agent and developer recommendations used while scaffolding this repo.

