from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, IPvAnyAddress


class LinkAccessBase(BaseModel):
    link_id: str
    ip_address: IPvAnyAddress
    params: Optional[str] = None


class LinkAccessCreate(LinkAccessBase):
    pass


class LinkAccessUpdate(LinkAccessBase):
    pass


class LinkAccessInDB(LinkAccessBase):
    id: int
    link_id: str
    ip_address: IPvAnyAddress
    params: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class LinkAccess(LinkAccessBase):
    pass


class LinkAccessCount(BaseModel):
    usages_count: int
