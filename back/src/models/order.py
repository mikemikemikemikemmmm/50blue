from sqlalchemy.orm import Mapped,relationship,mapped_column
from pydantic import BaseModel as BasePydanticSchema
from typing import List,TYPE_CHECKING
from datetime import datetime

from .order_item import ICE_CONTENT,SUGAR_CONTENT
from .base import BaseSQLModel,common_model_config_dict

if TYPE_CHECKING:
    from .order_item import OrderItemModel

class OrderModel(BaseSQLModel):
    __tablename__= "order"
    order_items : Mapped[List["OrderItemModel"]] =relationship(back_populates="order")
    total_price: Mapped[int]
    
class BaseSchema(BasePydanticSchema):
    order_item_ids : List[int]

class CreateSchema(BaseSchema):
    pass

    
class OrderItemReadSchemaForOrderRead(BasePydanticSchema):
    price:int
    ice_content:ICE_CONTENT
    sugar_content:SUGAR_CONTENT
    drink_id:int
    drink_name:str
    topping_name_list:List[str]
    
class ReadSchema(BasePydanticSchema):
    id: int
    created_at: str
    total_price: int
    order_items:List[OrderItemReadSchemaForOrderRead]
    model_config=common_model_config_dict
