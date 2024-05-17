from datetime import datetime
from typing import Optional

from pydantic import BaseModel, HttpUrl


class LinkBase(BaseModel):
    original_url: HttpUrl


class LinkCreate(LinkBase):
    id: Optional[str] = None


class LinkUpdate(BaseModel):
    has_deleted: bool


class LinkInDB(LinkBase):
    id: str
    created_at: datetime
    has_deleted: bool

    class Config:
        from_attributes = True


class Link(LinkInDB):
    pass
