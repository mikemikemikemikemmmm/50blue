from sqlalchemy.orm import Mapped, relationship, mapped_column
from pydantic import BaseModel as BasePydanticSchema
from typing import List, TYPE_CHECKING

from .base import BaseSQLModel, common_model_config_dict, UniqueNameMixin
from .order_topping_table import order_item_toppings_table

if TYPE_CHECKING:
    from .order_item import OrderItemModel


class ToppingModel(UniqueNameMixin, BaseSQLModel):
    __tablename__ = "topping"
    price: Mapped[int]
    order_item: Mapped[List["OrderItemModel"]] = relationship(
        secondary=order_item_toppings_table, back_populates="toppings"
    )


class BaseSchema(BasePydanticSchema):
    name: str
    price: int


class CreateSchema(BaseSchema):
    pass


class UpdateSchema(BaseSchema):
    pass


class ReadSchema(BaseSchema):
    id: int
    model_config = common_model_config_dict
