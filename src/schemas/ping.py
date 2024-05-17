from datetime import datetime

from pydantic import BaseModel


class Ping(BaseModel):
    status: str
    date: datetime
