from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from forkiteh.infrastructure.postgres.models.request import RequestOrm


class TestTronRouter:
    async def test_get_all_success(
        self,
        test_client: TestClient,
        postgres_session: AsyncSession,
        random_tron_wallet: str,
    ) -> None:
        postgres_session.add(RequestOrm(wallet_address=random_tron_wallet))
        await postgres_session.commit()

        response = test_client.get("/tron")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["items"][0]["wallet_address"] == random_tron_wallet
