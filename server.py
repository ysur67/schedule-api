import asyncclick as click
import uvicorn

from main import create_app


@click.group()
@click.pass_context
def cli(ctx):
    pass


@cli.command()
@click.option("--host", default="0.0.0.0")
@click.option("--port", default=8000)
async def runserver(host: str, port: int):
    app = await create_app()
    config = uvicorn.Config(app, host=host, port=port)
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    cli(_anyio_backend="asyncio")
