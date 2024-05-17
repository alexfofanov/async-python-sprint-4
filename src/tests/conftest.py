import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from db.db import engine
from main import app
from models import Base


@pytest_asyncio.fixture(scope='function')
async def async_client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url='http://test'
    ) as client:
        yield client


@pytest.fixture
def mock_client(mocker):
    return mocker.patch('fastapi.Request.client')


@pytest_asyncio.fixture
async def async_session() -> AsyncSession:
    session = async_sessionmaker(engine, expire_on_commit=False)

    async with session():
        async with engine.begin() as connect:
            await connect.run_sync(Base.metadata.create_all)

        yield session

    async with engine.begin() as connect:
        await connect.run_sync(Base.metadata.drop_all)

    await engine.dispose()
