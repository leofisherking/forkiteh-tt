from dishka import Scope, provide
from dishka.provider import Provider

from forkiteh.infrastructure.postgres.repositories.request_repository import (
    RequestsRepository,
)


class RepositoriesProvider(Provider):
    @provide(scope=Scope.APP)
    async def requests_repository(self) -> RequestsRepository:
        return RequestsRepository()
