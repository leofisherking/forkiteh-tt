from pydantic import computed_field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENV: str = "DEV"

    ALEMBIC_RECONNECT_INTERVAL: int = 1

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_SCHEMA: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_POOL_PRE_PING: bool = True
    MIN_POOL_SIZE: int = 10
    MAX_POOL_SIZE: int = 15

    TRON_API_KEY: str

    @computed_field
    def postgres_url(self) -> str:
        creds = f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
        return f"postgresql+asyncpg://{creds}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


settings = Settings()
