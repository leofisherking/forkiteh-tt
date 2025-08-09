from forkiteh.core.exceptions.tron import TronInvalidApiKey, TronWalletNotFound
from forkiteh.infrastructure.postgres.base import PostgresDatabase
from forkiteh.infrastructure.postgres.repositories.request_repository import (
    RequestsRepository,
)
from forkiteh.schemas.wallet_info import WalletInfoSchema
from forkiteh.schemas.wallet_request import CreateWalletRequestSchema
from forkiteh.services.tron_service import TronService


class GetWalletInfoUseCase:
    def __init__(
        self,
        database: PostgresDatabase,
        requests_repository: RequestsRepository,
        tron_service: TronService,
    ):
        self._database = database
        self._requests_repository = requests_repository
        self._tron_service = tron_service

    async def execute(self, wallet_address: str) -> WalletInfoSchema:
        try:
            result = await self._tron_service.get_wallet_info(
                wallet_address=wallet_address,
            )
        except (TronWalletNotFound, TronInvalidApiKey):
            raise

        async with self._database.session() as session:
            await self._requests_repository.create(
                session=session,
                create_schema=CreateWalletRequestSchema(wallet_address=wallet_address),
            )

        return result
