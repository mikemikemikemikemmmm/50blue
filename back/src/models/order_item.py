from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import ForeignKey
from pydantic import BaseModel as BasePydanticSchema
from typing import Literal, List, TYPE_CHECKING,Optional

from .base import BaseSQLModel, common_model_config_dict
from .order_topping_table import order_item_toppings_table
from .drink import  ReadSchema as DrinkRead
from .topping import  ReadSchema as ToppingRead

ICE_CONTENT = Literal["less", "regular", "half"]
SUGAR_CONTENT = Literal["less", "regular", "half"]

if TYPE_CHECKING:
    from .drink import DrinkModel, ReadSchema as DrinkRead
    from .topping import ToppingModel, ReadSchema as ToppingRead
    from .order import OrderModel


class OrderItemModel(BaseSQLModel):
    __tablename__ = "order_item"
    ice_content: Mapped[ICE_CONTENT]
    sugar_content: Mapped[SUGAR_CONTENT]
    price: Mapped[int]

    toppings: Mapped[List["ToppingModel"]] = relationship(
        secondary=order_item_toppings_table, back_populates="order_item"
    )

    drink_id: Mapped[int] = mapped_column(ForeignKey("drink.id"))
    drink: Mapped["DrinkModel"] = relationship(back_populates="order_items")
    
    order_id: Mapped[Optional[int]] = mapped_column(ForeignKey("order.id"))
    order: Mapped[Optional["OrderModel"]] = relationship(back_populates="order_items")


class BaseSchema(BasePydanticSchema):
    drink_id: int
    ice_content: ICE_CONTENT
    sugar_content: SUGAR_CONTENT
    topping_ids: List[int]


class CreateSchema(BaseSchema):
    pass


class ReadSchema(BaseSchema):
    id: int
    price: int
    drink: DrinkRead
    toppings: List[ToppingRead]
    model_config = common_model_config_dict
