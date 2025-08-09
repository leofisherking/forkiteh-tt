from dishka import Scope, provide
from dishka.provider import Provider

from forkiteh.infrastructure.postgres.base import PostgresDatabase


class InfrastructureProvider(Provider):
    @provide(scope=Scope.APP)
    async def postgres_database(self) -> PostgresDatabase:
        return PostgresDatabase()
