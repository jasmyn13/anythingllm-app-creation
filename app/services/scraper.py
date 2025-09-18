import asyncio
from typing import List


async def run_stub_scrape(source: str) -> List[dict]:
    # simulate network delay
    await asyncio.sleep(0.01)
    now = "2025-09-17T12:00:00Z"
    return [
        {"id": f"{source}-001", "url": "https://example.com/a", "title": "Stub A", "scraped_at": now, "source": source},
        {"id": f"{source}-002", "url": "https://example.com/b", "title": "Stub B", "scraped_at": now, "source": source},
    ]
