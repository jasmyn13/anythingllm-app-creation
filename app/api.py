from fastapi import APIRouter, HTTPException
from typing import List
from app.models import ItemOut
from scripts import store_data

router = APIRouter()


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.get("/items", response_model=List[ItemOut])
def get_items(limit: int = 100):
    conn = store_data.ensure_db("db/items.db")
    cur = conn.cursor()
    cur.execute("SELECT id, url, title, scraped_at, source FROM items ORDER BY scraped_at DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    items = [ItemOut(id=r[0], url=r[1], title=r[2], scraped_at=r[3], source=r[4]) for r in rows]
    return items


@router.post("/scrape")
async def trigger_scrape(source: str = "example"):
    # run a simple scrape stub and store results
    items = await store_data_run_stub(source)
    return {"inserted": items}


async def store_data_run_stub(source: str) -> int:
    # use the scraper service to get items
    from app.services.scraper import run_stub_scrape

    raw = await run_stub_scrape(source)
    items = [store_data.Item.from_dict(d) for d in raw]
    conn = store_data.ensure_db("db/items.db")
    inserted = store_data.store_items_sqlite(conn, items)
    return inserted
