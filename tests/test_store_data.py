import os
import sqlite3
import json
import tempfile

from scripts import store_data


def test_store_and_idempotent(tmp_path):
    # create temp db path
    db_path = tmp_path / "items.db"

    # load sample items from data folder
    sample_path = os.path.join(os.path.dirname(__file__), "..", "data", "sample_items.json")
    with open(sample_path, "r", encoding="utf-8") as f:
        sample = json.load(f)

    # ensure DB does not exist yet
    assert not db_path.exists()

    # store items first time
    conn = store_data.ensure_db(str(db_path))
    inserted = store_data.store_items_sqlite(conn, [store_data.Item.from_dict(d) for d in sample])
    assert inserted == 2

    # store again -> idempotent, should insert 0
    inserted2 = store_data.store_items_sqlite(conn, [store_data.Item.from_dict(d) for d in sample])
    assert inserted2 == 0

    # verify rows exist
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM items")
    count = cur.fetchone()[0]
    assert count == 2
