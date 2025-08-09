import asyncio
from decimal import Decimal
from typing import Any

from fastapi import status
from httpx import HTTPStatusError
from tronpy import AsyncTron
from tronpy.exceptions import AddressNotFound

from forkiteh.core.exceptions.tron import TronInvalidApiKey, TronWalletNotFound
from forkiteh.schemas.wallet_info import WalletInfoSchema


class TronService:
    def __init__(self, client: AsyncTron) -> None:
        self._client = client

    async def get_wallet_info(self, wallet_address: str) -> WalletInfoSchema:
        tasks = [
            self._get_balance(wallet_address),
            self._get_resources(wallet_address),
        ]

        try:
            res = await asyncio.gather(*tasks)
        except AddressNotFound:
            raise TronWalletNotFound(wallet_address=wallet_address)
        except HTTPStatusError as e:
            if e.response.status_code == status.HTTP_401_UNAUTHORIZED:
                raise TronInvalidApiKey()
            raise

        merged = {"wallet_address": wallet_address}
        for x in res:
            merged.update(x)

        return WalletInfoSchema.model_validate(merged)

    async def _get_balance(self, wallet_address: str) -> dict[str, Decimal]:
        balance: Decimal = await self._client.get_account_balance(wallet_address)
        return {"trx_balance": balance}

    async def _get_resources(self, wallet_address: str) -> dict[str, Any]:
        res = await self._client.get_account_resource(wallet_address)

        free_net_available = int(res.get("freeNetLimit", 0)) - int(
            res.get("freeNetUsed", 0),
        )
        staked_net_available = int(res.get("NetLimit", 0)) - int(res.get("NetUsed", 0))
        bandwidth_available = free_net_available + staked_net_available
        energy_available = int(res.get("EnergyLimit", 0)) - int(res.get("EnergyUsed", 0))

        return {
            "bandwidth": bandwidth_available,
            "energy": energy_available,
        }
