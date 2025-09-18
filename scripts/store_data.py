#!/usr/bin/env python3
"""scripts/store_data.py

Small utility to persist scraped items. Stores to a SQLite database by default and
can also dump to a JSON file. Designed to be lightweight and run locally.

Data shape expected: a list of objects with at least `id` or `url`, `title`, `scraped_at`.

Usage examples:
  python scripts/store_data.py --json-in data/sample_items.json
  python scripts/store_data.py --stdin-json  # read JSON array from stdin
  python scripts/store_data.py --json-in data/sample_items.json --db db/items.db
"""
from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Iterable, List, Optional


@dataclass
class Item:
    id: Optional[str]
    url: Optional[str]
    title: Optional[str]
    scraped_at: Optional[str]
    source: Optional[str] = None

    @staticmethod
    def from_dict(d: dict) -> "Item":
        return Item(
            id=d.get("id"),
            url=d.get("url"),
            title=d.get("title"),
            scraped_at=d.get("scraped_at") or d.get("scrapedAt") or datetime.utcnow().isoformat(),
            source=d.get("source"),
        )


def iter_items_from_stdin() -> Iterable[dict]:
    data = sys.stdin.read()
    if not data.strip():
        return []
    return json.loads(data)


def load_items_from_file(path: str) -> List[Item]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict):
        # allow top-level object with `items` key
        data = data.get("items", [])
    return [Item.from_dict(d) for d in data]


def ensure_db(path: str) -> sqlite3.Connection:
    os.makedirs(os.path.dirname(path), exist_ok=True) if os.path.dirname(path) else None
    conn = sqlite3.connect(path)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS items (
            pk INTEGER PRIMARY KEY AUTOINCREMENT,
            id TEXT,
            url TEXT,
            title TEXT,
            scraped_at TEXT,
            source TEXT,
            UNIQUE(id, url)
        )
        """
    )
    conn.commit()
    return conn


def store_items_sqlite(conn: sqlite3.Connection, items: Iterable[Item]) -> int:
    cur = conn.cursor()
    inserted = 0
    for it in items:
        try:
            cur.execute(
                "INSERT OR IGNORE INTO items (id, url, title, scraped_at, source) VALUES (?, ?, ?, ?, ?)",
                (it.id, it.url, it.title, it.scraped_at, it.source),
            )
            if cur.rowcount:
                inserted += 1
        except Exception:
            # keep going on bad rows
            continue
    conn.commit()
    return inserted


def dump_items_json(path: str, items: Iterable[Item]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True) if os.path.dirname(path) else None
    with open(path, "w", encoding="utf-8") as f:
        json.dump([asdict(i) for i in items], f, indent=2, ensure_ascii=False)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Store scraped items to SQLite/JSON")
    p.add_argument("--json-in", help="Path to JSON file containing an array of items")
    p.add_argument("--stdin-json", action="store_true", help="Read JSON array from stdin")
    p.add_argument("--db", default="db/items.db", help="SQLite DB path (default: db/items.db)")
    p.add_argument("--out-json", help="Optional: also write items to this JSON file")
    return p.parse_args()


def main() -> int:
    args = parse_args()

    raw: List[dict] = []
    if args.stdin_json:
        raw = list(iter_items_from_stdin())
    elif args.json_in:
        raw = load_items_from_file(args.json_in)
    else:
        print("No input provided. Use --json-in or --stdin-json.\n", file=sys.stderr)
        return 2

    # Normalize into Item objects
    items: List[Item]
    if raw and isinstance(raw[0], Item):
        items = raw  # type: ignore
    else:
        # When load_items_from_file returned Items already, raw will be Items; if read from stdin raw is dicts
        items = [Item.from_dict(d) if isinstance(d, dict) else d for d in raw]

    # Ensure DB and store
    conn = ensure_db(args.db)
    inserted = store_items_sqlite(conn, items)

    if args.out_json:
        dump_items_json(args.out_json, items)

    print(f"Stored {inserted} new items into {args.db}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
