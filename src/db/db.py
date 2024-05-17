from sys import modules

from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from core.config import app_settings

dsn = app_settings.dsn_test if 'pytest' in modules else app_settings.dsn

engine = create_async_engine(dsn, echo=True, future=True, poolclass=NullPool)
async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
