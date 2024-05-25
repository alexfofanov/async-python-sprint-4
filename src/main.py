import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from starlette.requests import Request
from starlette.responses import PlainTextResponse

from api.v1.base import api_router
from core.config import app_settings
from middleware.auth import AuthMiddleware
from middleware.blocking_access import BlockingAccessFromNetworksMiddleware

app = FastAPI(
    title=app_settings.app_title,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)

app.include_router(api_router, prefix='/api/v1')
app.add_middleware(BlockingAccessFromNetworksMiddleware)
app.add_middleware(AuthMiddleware, exclude_prefix='/api/v1/users/')


@app.exception_handler(RequestValidationError)
async def handle_error(
    request: Request, exc: RequestValidationError
) -> PlainTextResponse:
    return PlainTextResponse(str(exc.errors()), status_code=400)


if __name__ == '__main__':
    host = app_settings.project_host
    uvicorn.run(
        'main:app',
        host=str(app_settings.project_host),
        port=app_settings.project_port,
        reload=True,
    )
