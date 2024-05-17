import datetime
from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_session
from schemas.ping import Ping
from services.ping import ping as check_database_status

ping_router = APIRouter()


@ping_router.get('/', response_model=Ping)
async def ping(
    db: AsyncSession = Depends(get_session),
) -> Any:
    """
    Проверка статуса доступности БД
    """

    status = await check_database_status(db=db)
    return {
        'status': 'OK' if status else 'not available',
        'date': datetime.datetime.utcnow(),
    }
