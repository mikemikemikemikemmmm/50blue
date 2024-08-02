from sqlalchemy import create_engine,select
from sqlalchemy.orm import sessionmaker,Session
from typing import Annotated
from fastapi import Depends
from src.setting.index import get_settings
SQLALCHEMY_DATABASE_URL = get_settings().SQLALCHEMY_DATABASE_URL
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    isolation_level="SERIALIZABLE"
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


SessionDepend = Annotated[Session, Depends(get_db)]
