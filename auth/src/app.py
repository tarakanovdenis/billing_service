from contextlib import asynccontextmanager

from fastapi import FastAPI
from redis.asyncio import Redis
from fastapi_pagination import add_pagination

from src.db import redis
from src.core.config import settings
from src.routers.auth import router as auth_router
from src.routers.admin import router as admin_router
from src.routers.user import router as user_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    redis.redis = Redis(
        host=settings.service_settings.redis_host,
        port=settings.service_settings.redis_port,
        db=1
    )
    yield
    await redis.redis.close()


application = FastAPI(
    lifespan=lifespan,
    title=settings.project_settings.title,
    docs_url=settings.project_settings.docs_url,
    openapi_url=settings.project_settings.openapi_url,
    description=settings.project_settings.description,
    version=settings.project_settings.version,
)
application.include_router(
    admin_router, prefix='/auth/admin', tags=['Admin Endpoints']
)
application.include_router(
    auth_router, prefix='/auth', tags=['Auth Endpoints']
)
application.include_router(
    user_router, prefix='/auth/user', tags=['User Endpoints']
)

add_pagination(application)
