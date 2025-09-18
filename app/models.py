from pydantic import BaseModel
from typing import Optional


class ItemOut(BaseModel):
    id: Optional[str]
    url: Optional[str]
    title: Optional[str]
    scraped_at: Optional[str]
    source: Optional[str]

    class Config:
        orm_mode = True
