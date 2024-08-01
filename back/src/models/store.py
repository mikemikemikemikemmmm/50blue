from sqlalchemy.orm import Mapped,mapped_column
from pydantic import BaseModel as BasePydanticSchema

from .base import BaseSQLModel,common_model_config_dict,UniqueNameMixin

class StoreModel(UniqueNameMixin,BaseSQLModel):
    __tablename__= "store"

class BaseSchema(BasePydanticSchema):
    name:str

class CreateSchema(BaseSchema):
    pass

class UpdateSchema(BaseSchema):
    pass

class ReadSchema(BaseSchema):
    id:int
    model_config=common_model_config_dict