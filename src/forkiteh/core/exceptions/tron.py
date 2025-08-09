from typing import Final


class TronInvalidApiKey(Exception):
    _ERROR_MESSAGE: Final[str] = "Invalid Tron API key"

    def __init__(self) -> None:
        self.message = self._ERROR_MESSAGE
        super().__init__(self.message)


class TronWalletNotFound(Exception):
    _ERROR_MESSAGE: Final[str] = "Wallet not found {wallet_address}"

    def __init__(self, wallet_address: str) -> None:
        self.message = self._ERROR_MESSAGE.format(wallet_address=wallet_address)
        super().__init__(self.message)
