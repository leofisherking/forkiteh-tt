from pydantic import BaseModel, field_validator
from tronpy.keys import is_base58check_address


class GetWalletInfoPayload(BaseModel):
    wallet_address: str

    @field_validator("wallet_address")
    def validate_tron_address(cls, v: str) -> str:
        if not is_base58check_address(v):
            raise ValueError("Invalid TRON address format")
        return v
