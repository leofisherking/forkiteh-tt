from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator
from tronpy.keys import is_base58check_address


class BaseWalletRequestSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    wallet_address: str

    @field_validator("wallet_address")
    def validate_tron_address(cls, v: str) -> str:
        if not is_base58check_address(v):
            raise ValueError("Invalid TRON address format")
        return v


class CreateWalletRequestSchema(BaseWalletRequestSchema):
    pass


class WalletRequestSchema(BaseWalletRequestSchema):
    id: int
    created_at: datetime
