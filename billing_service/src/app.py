from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
# from redis.asyncio import Redis
# from fastapi_pagination import add_pagination

from src.db.mongodb import get_mongodb_client
from src.core.config import BASE_DIR, settings
from src.routers.profile import router as profile_router
from src.routers.currency import router as currency_router
from src.routers.currency_pair import router as currency_pair_router
from src.routers.bank_account import router as bank_account_router
from src.routers.admin_profiles import router as admin_profile_router
from src.routers.admin_bank_accounts import router as admin_bank_account_router
from src.routers.payment_service import router as payment_service_router
from src.routers.transaction import router as transaction_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    await get_mongodb_client(
        settings.mongodb_settings.mongodb_host,
        settings.mongodb_settings.mongodb_port,
        settings.mongodb_settings.mongodb_db_name,
    )
    # redis.redis = Redis(
    #     host=settings.service_settings.redis_host,
    #     port=settings.service_settings.redis_port,
    #     db=1
    # )
    yield
    # await redis.redis.close()


application = FastAPI(
    lifespan=lifespan,
    title=settings.project_settings.title,
    docs_url=settings.project_settings.docs_url,
    openapi_url=settings.project_settings.openapi_url,
    description=settings.project_settings.description,
    version=settings.project_settings.version,
)
application.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)
application.include_router(
    profile_router,
    prefix="/billing/profile",
    tags=["Profile Endpoints"],
)
application.include_router(
    bank_account_router,
    prefix="/billing/bank-account",
    tags=["Bank Account Endpoints"],
)
application.include_router(
    currency_router,
    prefix="/billing/currency",
    tags=["Admin Currency CRUD"],
)
application.include_router(
    currency_pair_router,
    prefix="/billing/currency-pair",
    tags=["Admin Currency Pair CRUD"],
)
application.include_router(
    admin_profile_router,
    prefix="/billing/admin/profiles",
    tags=["Admin Profile Endpoints"],
)
application.include_router(
    admin_bank_account_router,
    prefix="/billing/admin/bank-accounts",
    tags=["Admin Bank Account Endpoints"],
)
application.include_router(
    payment_service_router,
    prefix="/billing/payment",
    tags=["Payment Endpoints"],
)
application.include_router(
    transaction_router,
    prefix="/billing/transactions",
    tags=["Transaction History Endpoints"],
)

# add_pagination(application)
