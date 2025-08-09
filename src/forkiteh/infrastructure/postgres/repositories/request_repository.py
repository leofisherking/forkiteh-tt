from typing import Type

from sqlalchemy import Select, func, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from forkiteh.infrastructure.postgres.models.request import RequestOrm
from forkiteh.schemas.wallet_request import (
    CreateWalletRequestSchema,
    WalletRequestSchema,
)


class RequestsRepository:
    _collection: Type[RequestOrm] = RequestOrm

    async def create(
        self,
        session: AsyncSession,
        create_schema: CreateWalletRequestSchema,
    ) -> WalletRequestSchema:
        query = (
            insert(self._collection)
            .values(**create_schema.model_dump())
            .returning(self._collection)
        )

        result = await session.scalar(query)

        return WalletRequestSchema.model_validate(result)

    async def get_all(
        self,
        session: AsyncSession,
        limit: int = 100,
        offset: int = 0,
    ) -> tuple[list[WalletRequestSchema], int]:
        query = (
            select(self._collection)
            .order_by(self._collection.created_at.desc())
            .limit(limit)
            .offset(offset)
        )

        result = await session.scalars(query)
        total = await self._get_total(session=session, query=query)

        return [WalletRequestSchema.model_validate(x) for x in result], total

    @staticmethod
    async def _get_total(session: AsyncSession, query: Select) -> int:
        clean_query = query.limit(None).offset(None)

        count_query = select(func.count()).select_from(clean_query.subquery())
        result = await session.scalar(count_query)
        return result if result is not None else 0
