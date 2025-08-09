from collections.abc import AsyncGenerator

from dishka import Provider, Scope, provide
from tronpy import AsyncTron
from tronpy.providers import AsyncHTTPProvider

from forkiteh.core.settings import settings
from forkiteh.services.tron_service import TronService


class ServicesProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def tron_service(self) -> AsyncGenerator[TronService]:
        async with AsyncTron(
            provider=AsyncHTTPProvider(api_key=settings.TRON_API_KEY),
        ) as client:
            yield TronService(client=client)
