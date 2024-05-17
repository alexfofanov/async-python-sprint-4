from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, String

from .base import Base


class Link(Base):
    """
    Ссылка
    """

    __tablename__ = 'link'

    id = Column(String, primary_key=True)
    original_url = Column(String, nullable=False)
    created_at = Column(
        DateTime, nullable=False, index=True, default=datetime.utcnow
    )
    has_deleted = Column(Boolean, nullable=False, default=False)
