import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.di.container import Container
from routers.group import router as groups_router
from routers.lesson import router as lessons_router
from routers.teacher import router as teachers_router


async def create_app() -> FastAPI:
    app = FastAPI()
    container = Container()
    container.wire(sys.modules[__name__])
    await container.init_resources()
    _ = await container.db_session()
    app.container = container
    origins = [
        "http://localhost:3000",
        "http://localhost:4321",
        "http://172.31.157.168:3000",
        "http://192.168.0.104:3000"
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(
        groups_router,
        prefix="/api/v1"
    )
    app.include_router(
        teachers_router,
        prefix="/api/v1"
    )
    app.include_router(
        lessons_router,
        prefix="/api/v1"
    )
    return app
