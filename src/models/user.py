from datetime import datetime

from sqlalchemy import Column, DateTime, String, Integer

from .base import Base


class User(Base):
    """
    Пользователь
    """

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    login = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(
        DateTime, nullable=False, index=True, default=datetime.utcnow
    )
