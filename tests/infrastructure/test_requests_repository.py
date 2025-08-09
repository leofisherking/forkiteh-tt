from sqlalchemy.ext.asyncio import AsyncSession

from forkiteh.infrastructure.postgres.repositories.request_repository import (
    RequestsRepository,
)
from forkiteh.schemas.wallet_request import (
    CreateWalletRequestSchema,
    WalletRequestSchema,
)


class TestRequestsRepository:
    async def test_create_success(
        self,
        random_request_create_schema: CreateWalletRequestSchema,
        requests_repository: RequestsRepository,
        postgres_session: AsyncSession,
    ) -> None:
        created_request: WalletRequestSchema = await requests_repository.create(
            session=postgres_session,
            create_schema=random_request_create_schema,
        )

        assert (
            created_request.wallet_address == random_request_create_schema.wallet_address
        )
