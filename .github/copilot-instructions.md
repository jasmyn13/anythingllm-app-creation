<!-- .github/copilot-instructions.md - Guidance for AI coding agents in this repo -->
# Guidance for AI coding agents

This repository is small and currently contains only a top-level `README.md`. The project goal (from the README) is to build an AnythingLLM-based app that hosts a website and scrapes new information daily.

Keep instructions concise and actionable. Only implement or suggest changes that can be validated from files in the workspace, or that are clearly requested by the repo owner.

Key context and expectations
- Big picture: a web-hosted app that uses AnythingLLM to process or surface newly-scraped information daily. The repo currently has no source code or build config; treat proposed code as scaffolding until the owner adds more files.
- Minimal starting files: `README.md` (project intent). No package manifests, test suites, or CI workflows were found.

What to do first when asked to implement features
- Create minimal, runnable scaffolding: include a small server (Flask/FastAPI for Python or Express/Vite for JS) plus a README update and a simple start script (`package.json` or `requirements.txt` + run instruction).
- Prefer small, self-contained modules. Add tests (one happy path) and a README section showing how to run locally.

Conventions and patterns to follow (repo-discoverable)
- Favor explicit files for runtime and dependencies: `package.json` / `requirements.txt` / `pyproject.toml` depending on language chosen. Avoid assuming an environment beyond what is added.
- Add a short `README.md` change that documents new commands and any new files you add.
- When adding scraping components: keep scraping separate from web-serving logic (e.g., a `scraper/` package or `tasks/scrape.py`) and expose a simple API endpoint that returns the latest scraped items.

Examples (when scaffolding)
- Node.js minimal: add `package.json`, `server.js` (Express), `scraper/cron.js` (daily scrape stub), and a `README.md` section with `npm install` and `npm start`.
- Python minimal: add `pyproject.toml` or `requirements.txt`, `app.py` (FastAPI), `scraper/scrape.py`, and a `README.md` section with `pip install -r requirements.txt` and `uvicorn app:app --reload`.

Integration & external dependencies
- If adding AnythingLLM integration, add a clear config file or `.env` example (do NOT include secrets). Use `ANYTHINGLLM_API_KEY` as the variable name in examples.
- When proposing third-party services (hosting, scheduling), provide an option for a local fallback (cron job / background worker) so the owner can test locally.

Developer workflows (what to document when you add files)
- How to install dependencies and run the app locally (exact commands).
- How to run any tests you add (e.g., `npm test` or `pytest -q`).
- How to trigger the scraper manually and how the daily schedule is expected to run (cron, GitHub Actions, or platform scheduler).

Editing policy for AI agents
- Only change or add files when the user asks. When creating new code, keep changes minimal and testable.
- When modifying `README.md` or other docs, keep the project intent consistent with the original `README.md`.
- Do not invent deployment credentials or make network calls. Provide instructions and optional commands for the human to run locally.

Where to reference in PRs
- Always point to the files you added (e.g., `server.js`, `scraper/scrape.py`, `package.json`) and include a short testing checklist in the PR description:
  - install dependencies
  - run the server
  - run the scrape stub and confirm output

Questions for the repo owner
- Which language / runtime do you prefer for scaffolding (Node.js or Python)?
- Do you already have an AnythingLLM account / API details, or should we stub integration and document how to wire it up?

If you want a different structure, reply with the preferred stack and I will create the initial scaffold and tests.
