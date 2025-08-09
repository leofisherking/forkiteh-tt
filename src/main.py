import asyncio

from uvicorn import Config, Server

from forkiteh.app import create_app


async def run() -> None:
    app = create_app()

    config = Config(
        app=app,
        host="0.0.0.0",
        port=8000,
    )
    server = Server(config=config)

    tasks = (asyncio.create_task(server.serve()),)

    await asyncio.wait(
        tasks,
        return_when=asyncio.FIRST_COMPLETED,
    )


if __name__ == "__main__":
    asyncio.run(run())
