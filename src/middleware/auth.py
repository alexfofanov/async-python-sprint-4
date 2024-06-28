from fastapi import HTTPException, Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from core.auth import get_current_user

ACCESS_TOKEN_POS = 1


class AuthMiddleware(BaseHTTPMiddleware):
    """
    Авторизация пользователя
    """

    def __init__(self, app, exclude_prefixes: list[str]):
        super().__init__(app)
        self.exclude_prefixes = exclude_prefixes

    async def dispatch(self, request: Request, call_next):
        for exclude_prefix in self.exclude_prefixes:
            if request.url.path.startswith(exclude_prefix):
                return await call_next(request)

        authorization: str = request.headers.get('authorization')
        if authorization and len(authorization.split()) == 2:
            try:
                user = await get_current_user(
                    authorization.split()[ACCESS_TOKEN_POS]
                )
            except HTTPException as e:
                return JSONResponse(
                    status_code=e.status_code,
                    content={"detail": e.detail},
                    headers=e.headers,
                )

        else:
            return Response(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content='Error on authorization header',
            )

        request.state.user = user
        return await call_next(request)
