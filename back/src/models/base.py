
from sqlalchemy import Column, DateTime, func,Integer,String
from sqlalchemy.orm import DeclarativeBase,registry,mapped_column,Mapped
from sqlalchemy.ext.declarative import declared_attr
from pydantic import ConfigDict
from typing import Annotated

class Base(DeclarativeBase):
    pass

class BaseSQLModel(Base):
    __abstract__ = True
    @declared_attr
    def created_at(cls):
        return Column(
            DateTime, 
            default=func.now(), 
            nullable=False)

    @declared_attr
    def updated_at(cls):
        return Column(
            DateTime,
            default=func.now(),
            onupdate=func.now(),
            nullable=False,
        )
    @declared_attr
    def id(cls):
        return Column(Integer,autoincrement=True, primary_key=True)
    
class UniqueNameMixin:
    name: Mapped[str] = mapped_column(unique=True)
    
common_model_config_dict = ConfigDict(
         from_attributes=True,
        #  extra="forbid",
        #  validate_assignment=True,
    )
