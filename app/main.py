from fastapi import FastAPI
from app.api import router as api_router
import uvicorn

app = FastAPI(title="AnythingLLM Scraper")

app.include_router(api_router)


def run(host: str = "0.0.0.0", port: int = 8000, reload: bool = True):
	"""Programmatic entrypoint so the app can be run with `python -m app.main`."""
	uvicorn.run("app.main:app", host=host, port=port, reload=reload)


if __name__ == "__main__":
	run()
