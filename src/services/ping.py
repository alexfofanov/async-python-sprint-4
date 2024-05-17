from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


async def ping(db: AsyncSession) -> bool | None:
    try:
        await db.execute(text('SELECT 1'))
    except Exception as error:
        raise HTTPException(
            status_code=500, detail=f'Database is not available {error}'
        )
    return True
