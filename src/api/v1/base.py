from fastapi import APIRouter

from api.v1.link import link_router
from api.v1.ping import ping_router
from api.v1.user import user_router

api_router = APIRouter()
api_router.include_router(link_router, prefix='/links', tags=['links'])
api_router.include_router(ping_router, prefix='/ping', tags=['ping'])
api_router.include_router(user_router, prefix='/users', tags=['user'])
