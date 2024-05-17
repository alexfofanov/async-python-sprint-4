from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.link import Link as LinkModel
from schemas.link import LinkCreate, LinkUpdate

from .base import CreateSchemaType, ModelType, RepositoryDB


class RepositoryLink(RepositoryDB[LinkModel, LinkCreate, LinkUpdate]):
    async def get_multi(
        self, db: AsyncSession, *, offset: int, limit: int
    ) -> list[ModelType]:
        stmt = (
            select(self._model)
            .where(self._model.has_deleted == False)  # noqa: E712
            .offset(offset)
            .limit(limit)
        )
        results = await db.execute(statement=stmt)
        return results.scalars().all()

    async def create_batch(
        self, db: AsyncSession, *, objs: list[CreateSchemaType]
    ) -> list[ModelType]:
        db_objs = [
            obj.dict() | {'original_url': str(obj.original_url)}
            for obj in objs
        ]
        stmt = insert(self._model).values(db_objs).returning(self._model)
        result = await db.execute(stmt)
        await db.commit()
        return result.scalars().all()


link_crud = RepositoryLink(LinkModel)
