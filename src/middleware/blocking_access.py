import ipaddress
import logging.config

from fastapi import Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware

from core.config import app_settings
from core.logger import LOGGING

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


class BlockingAccessFromNetworksMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        host = request.client.host
        if self.is_ip_blocked(host):
            logger.info(f'Blocking access from ip {host}')
            return Response(
                status_code=status.HTTP_403_FORBIDDEN, content='Access denied'
            )

        return await call_next(request)

    @staticmethod
    def is_ip_blocked(ip_address):
        for subnet in app_settings.block_subnets:
            if ipaddress.ip_address(ip_address) in ipaddress.ip_network(
                subnet
            ):
                return True
        return False
