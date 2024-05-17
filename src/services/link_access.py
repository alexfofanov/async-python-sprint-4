from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.link_access import LinkAccess as LinkAccessModel
from schemas.link_access import LinkAccessCreate, LinkAccessUpdate

from .base import ModelType, RepositoryDB


class RepositoryLinkAccess(
    RepositoryDB[LinkAccessModel, LinkAccessCreate, LinkAccessUpdate]
):
    async def get_status(self, db: AsyncSession, id: str) -> tuple[int] | None:
        stmt = (
            select(func.count().label('usages_count'))
            .select_from(self._model)
            .where(self._model.link_id == id)
        )
        result = await db.execute(statement=stmt)
        return result.first()

    async def get_full_status(
        self, db: AsyncSession, id: str, offset: int, limit: int
    ) -> list[ModelType]:
        stmt = (
            select(self._model)
            .where(self._model.link_id == id)
            .offset(offset)
            .limit(limit)
        )
        results = await db.execute(statement=stmt)
        return results.scalars().all()


link_access_crud = RepositoryLinkAccess(LinkAccessModel)
