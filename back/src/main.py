from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.middleware.index import setup_global_middleware
from src.errorHandler.index import setup_global_error_handler
from src.models import *
from src.db.engine import engine
from src.models.base import Base
from src.api.root import router as root_router
from src.utils.index import is_dev_environment, get_environment
from src.setting.index import get_settings

setting = get_settings()
print(setting.FRONT_ORIGIN)

@asynccontextmanager
async def lifespan(app: FastAPI):
    if is_dev_environment():
        print("create db")
        # Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(root_router)
setup_global_error_handler(app)
setup_global_middleware(app)
