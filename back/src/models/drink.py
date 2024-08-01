from sqlalchemy.orm import Mapped,relationship,mapped_column
from pydantic import BaseModel as BasePydanticSchema
from typing import List,TYPE_CHECKING

from .base import BaseSQLModel,common_model_config_dict,UniqueNameMixin

if TYPE_CHECKING:
    from .order_item import OrderItemModel

class DrinkModel(UniqueNameMixin,BaseSQLModel):
    __tablename__= "drink"
    order_items: Mapped[List["OrderItemModel"]] = relationship(back_populates="drink")
    price: Mapped[int]

class BaseSchema(BasePydanticSchema):
    name:str
    price:int

class CreateSchema(BaseSchema):
    pass

class UpdateSchema(BaseSchema):
    pass

class ReadSchema(BaseSchema):
    id:int
    model_config=common_model_config_dict