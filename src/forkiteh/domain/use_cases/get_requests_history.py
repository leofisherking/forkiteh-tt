from forkiteh.infrastructure.postgres.base import PostgresDatabase
from forkiteh.infrastructure.postgres.repositories.request_repository import (
    RequestsRepository,
)
from forkiteh.schemas.wallet_request import WalletRequestSchema


class GetRequestsUseCase:
    def __init__(
        self,
        database: PostgresDatabase,
        requests_repository: RequestsRepository,
    ) -> None:
        self._database = database
        self._requests_repository = requests_repository

    async def execute(
        self,
        limit: int = 100,
        offset: int = 0,
    ) -> tuple[list[WalletRequestSchema], int]:
        async with self._database.session() as session:
            return await self._requests_repository.get_all(
                session=session,
                limit=limit,
                offset=offset,
            )
