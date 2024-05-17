from secrets import token_urlsafe
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import app_settings
from db.db import get_session
from schemas.link import Link, LinkCreate, LinkUpdate
from schemas.link_access import LinkAccess, LinkAccessCount, LinkAccessCreate
from services.link import link_crud
from services.link_access import link_access_crud

link_router = APIRouter()


@link_router.get('/', response_model=list[Link])
async def get_links(
    db: AsyncSession = Depends(get_session),
    offset: int = 0,
    limit: int = 10,
) -> Any:
    """
    Список ссылок
    """

    links = await link_crud.get_multi(db=db, offset=offset, limit=limit)
    return links


@link_router.get(
    '/{id}/status', response_model=list[LinkAccess] | LinkAccessCount
)
async def get_link_status(
    request: Request,
    *,
    db: AsyncSession = Depends(get_session),
    id: str,
    full_info: bool = Query(default=False),
    offset: int = Query(default=0),
    limit: int = Query(default=10),
) -> Any:
    """
    Получение данных по использованию ссылки
    """

    link = await link_crud.get(db=db, id=id)
    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Link not found'
        )

    if link.has_deleted:
        raise HTTPException(
            status_code=status.HTTP_410_GONE, detail='Link is deleted'
        )

    if full_info:
        link_access = await link_access_crud.get_full_status(
            db=db, id=id, offset=offset, limit=limit
        )
        return link_access

    link_usages_count = await link_access_crud.get_status(db=db, id=id)

    return link_usages_count


@link_router.get('/{id}')
async def get_link(
    request: Request,
    *,
    db: AsyncSession = Depends(get_session),
    id: str,
) -> Any:
    """
    Ссылка
    """

    link = await link_crud.get(db=db, id=id)
    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Link not found'
        )

    if link.has_deleted:
        raise HTTPException(
            status_code=status.HTTP_410_GONE, detail='Link is deleted'
        )

    obj = LinkAccessCreate(
        link_id=id,
        ip_address=request.client.host,
        params=str(request.query_params),
    )
    await link_access_crud.create(db=db, obj=obj)

    return RedirectResponse(
        link.original_url,
        status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    )


@link_router.post(
    '/', response_model=Link, status_code=status.HTTP_201_CREATED
)
async def create_link(
    *,
    db: AsyncSession = Depends(get_session),
    obj: LinkCreate,
) -> Any:
    """
    Создание ссылки
    """

    obj.id = token_urlsafe(app_settings.token_size)
    link = await link_crud.create(db=db, obj=obj)
    return link


@link_router.post(
    '/batch', response_model=list[Link], status_code=status.HTTP_201_CREATED
)
async def create_link_batch(
    *,
    db: AsyncSession = Depends(get_session),
    objs: list[LinkCreate],
) -> Any:
    """
    Создание пачки ссылок
    """

    for obj in objs:
        obj.id = token_urlsafe(app_settings.token_size)
    links = await link_crud.create_batch(db=db, objs=objs)
    return links


@link_router.delete('/{id}', response_model=Link)
async def delete_link(
    *,
    db: AsyncSession = Depends(get_session),
    id: str,
) -> Any:
    """
    Удаление ссылки
    """

    link = await link_crud.get(db=db, id=id)
    if link and link.has_deleted:
        raise HTTPException(
            status_code=status.HTTP_410_GONE, detail='Link is deleted'
        )

    link = await link_crud.patch(
        db=db, id=id, data=LinkUpdate(has_deleted=True)
    )
    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Link not found"
        )

    return link


@link_router.patch('/{id}', response_model=Link)
async def update_link(
    *,
    db: AsyncSession = Depends(get_session),
    id: int,
    data: LinkUpdate,
) -> Any:
    """
    Изменение ссылки
    """

    link = await link_crud.patch(db=db, id=id, data=data)
    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Link not found"
        )

    return link
