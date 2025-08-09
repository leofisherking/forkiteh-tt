from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class WalletInfoSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    wallet_address: str
    bandwidth: int
    energy: int
    trx_balance: Decimal
