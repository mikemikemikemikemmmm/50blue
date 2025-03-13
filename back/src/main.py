from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.middleware.index import setup_global_middleware
from src.errorHandler.index import setup_global_error_handler
from src.models import *
# from src.db.engine import engine
# from src.models.base import Base
from src.api.root import router as root_router
from src.utils.index import is_dev_environment
from src.setting.index import get_settings

setting = get_settings()


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     if is_dev_environment():
#         # print("create db")
#         # # Base.metadata.drop_all(bind=engine)
#         # Base.metadata.create_all(bind=engine)
#     yield

is_dev = is_dev_environment()
app = FastAPI(
    # lifespan=lifespan,
    docs_url="/docs" if is_dev else None,
    redoc_url="/redoc" if is_dev else None,
    openapi_url="/openapi.json" if is_dev else None
)
app.include_router(root_router)
setup_global_error_handler(app)
setup_global_middleware(app)
