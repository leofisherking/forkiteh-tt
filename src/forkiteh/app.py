from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from dishka.integrations.fastapi import setup_dishka as setup_dishka_fastapi
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from forkiteh.api.router import router as tron_router
from forkiteh.core.providers.setup import app_container
from forkiteh.core.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any]:
    yield

    await app.state.dishka_container.close()


def create_app() -> FastAPI:
    app_options = {}
    if settings.ENV == "PROD":
        app_options = {
            "docs_url": None,
            "redoc_url": None,
        }

    app = FastAPI(
        title="Forkiteh Tron",
        lifespan=lifespan,
        **app_options,  # type: ignore
    )

    app.include_router(tron_router, tags=["Tron"])

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_credentials=True,
    )

    setup_dishka_fastapi(
        container=app_container,
        app=app,
    )

    return app
