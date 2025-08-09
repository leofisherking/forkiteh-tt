from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from forkiteh.core.settings import settings


class PostgresDatabase:
    def __init__(self) -> None:
        self._engine = create_async_engine(
            settings.postgres_url,
            pool_size=settings.MIN_POOL_SIZE,
            max_overflow=settings.MAX_POOL_SIZE,
            pool_pre_ping=settings.POSTGRES_POOL_PRE_PING,
        )
        self._session_factory = async_sessionmaker(
            bind=self._engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
            class_=AsyncSession,
        )

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession]:
        async with self._session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise


metadata = MetaData(schema=settings.POSTGRES_SCHEMA)


class Base(DeclarativeBase):
    metadata = metadata
