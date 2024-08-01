import os
from functools import lru_cache
from dotenv import load_dotenv

class Settings():
    ENVIRONMENT: str = str(os.getenv("ENVIRONMENT"))
    FRONT_ORIGIN:str = str(os.getenv("FRONT_ORIGIN"))
    SQLALCHEMY_DATABASE_URL: str = str(os.getenv("SQLALCHEMY_DATABASE_URL"))

    #auth
    SECRET_KEY: str = str(os.getenv("SECRET_KEY"))
    ALGORITHM: str = str(os.getenv("ALGORITHM"))
    ACCESS_TOKEN_EXPIRE_MINUTES = str(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    # REFRESH_TOKEN_EXPIRE_DAYS = str(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))

@lru_cache()
def get_settings():
    load_dotenv( f".env.{os.getenv('ENVIRONMENT')}")
    return Settings()