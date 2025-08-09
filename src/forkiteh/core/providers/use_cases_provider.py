from dishka import Provider, Scope, provide

from forkiteh.domain.use_cases.get_requests_history import GetRequestsUseCase
from forkiteh.domain.use_cases.get_wallet_info import GetWalletInfoUseCase
from forkiteh.infrastructure.postgres.base import PostgresDatabase
from forkiteh.infrastructure.postgres.repositories.request_repository import (
    RequestsRepository,
)
from forkiteh.services.tron_service import TronService


class UseCasesProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_requests(
        self,
        database: PostgresDatabase,
        requests_repository: RequestsRepository,
    ) -> GetRequestsUseCase:
        return GetRequestsUseCase(
            database=database,
            requests_repository=requests_repository,
        )

    @provide(scope=Scope.REQUEST)
    async def get_wallet_info(
        self,
        database: PostgresDatabase,
        requests_repository: RequestsRepository,
        tron_service: TronService,
    ) -> GetWalletInfoUseCase:
        return GetWalletInfoUseCase(
            database=database,
            requests_repository=requests_repository,
            tron_service=tron_service,
        )
