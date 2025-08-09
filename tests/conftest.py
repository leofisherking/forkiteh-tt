from typing import AsyncGenerator, Generator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from tronpy.keys import PrivateKey

from alembic import command
from alembic.config import Config

from forkiteh.app import create_app
from forkiteh.core.settings import Settings
from forkiteh.core.settings import settings as app_settings
from forkiteh.infrastructure.postgres.base import PostgresDatabase
from forkiteh.infrastructure.postgres.repositories.request_repository import (
    RequestsRepository,
)
from fastapi.testclient import TestClient

from forkiteh.schemas.wallet_request import CreateWalletRequestSchema


@pytest.fixture(scope="module")
async def settings() -> Settings:
    return app_settings


@pytest.fixture(scope="function", autouse=True)
def apply_migrations(settings: Settings) -> Generator[None]:
    alembic_config = Config("alembic.ini")

    command.upgrade(config=alembic_config, revision="head")
    yield
    command.downgrade(
        config=alembic_config,
        revision="base",
    )


@pytest.fixture()
def test_client() -> TestClient:
    return TestClient(create_app())


@pytest.fixture
async def postgres_database() -> PostgresDatabase:
    return PostgresDatabase()


@pytest.fixture
async def postgres_session(
    postgres_database: PostgresDatabase,
) -> AsyncGenerator[AsyncSession]:
    async with postgres_database.session() as session:
        yield session


@pytest.fixture
async def requests_repository() -> AsyncGenerator[RequestsRepository]:
    yield RequestsRepository()


@pytest.fixture
async def random_tron_wallet() -> str:
    return PrivateKey.random().public_key.to_base58check_address()


@pytest.fixture
async def random_request_create_schema(
    random_tron_wallet: str,
) -> CreateWalletRequestSchema:
    return CreateWalletRequestSchema(
        wallet_address=random_tron_wallet,
    )
