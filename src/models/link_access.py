from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from .base import Base


class LinkAccess(Base):
    """
    Доступ к ссылке
    """

    __tablename__ = 'link_access'

    id = Column(Integer, primary_key=True)
    link_id = Column(
        String, ForeignKey('link.id', ondelete='CASCADE'), nullable=False
    )
    ip_address = Column(String, nullable=False)
    params = Column(String, nullable=True)
    created_at = Column(
        DateTime, nullable=False, index=True, default=datetime.utcnow
    )
