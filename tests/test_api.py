import os
import json
import tempfile

import pytest
from fastapi.testclient import TestClient

import app.main as main_mod


@pytest.fixture
def client(tmp_path, monkeypatch):
    # monkeypatch ensure_db to create a temp db per test
    db_path = str(tmp_path / "test_items.db")

    # Import the module and capture the original ensure_db so our replacement
    # can delegate to the real implementation without recursing into itself.
    import scripts.store_data as sd
    _orig_ensure = sd.ensure_db

    def ensure_db(path: str = db_path):
        # delegate to the real function but force our path
        return _orig_ensure(db_path)

    monkeypatch.setattr(sd, "ensure_db", ensure_db)

    client = TestClient(main_mod.app)
    yield client


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_items_and_scrape(client):
    # ensure items endpoint empty initially
    r = client.get("/items")
    assert r.status_code == 200
    assert isinstance(r.json(), list)

    # call scrape endpoint to insert stub items
    r2 = client.post("/scrape")
    assert r2.status_code == 200
    data = r2.json()
    assert "inserted" in data

    # now ensure /items returns entries
    r3 = client.get("/items")
    assert r3.status_code == 200
    items = r3.json()
    assert len(items) >= 2
