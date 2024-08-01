from sqlalchemy import ForeignKey,Table,Column

from .base import Base as BaseSQLModel

order_item_toppings_table = Table(
    "order_item_toppings",
    BaseSQLModel.metadata,
    Column("topping_id", ForeignKey("topping.id"),primary_key=True),
    Column("order_item_id", ForeignKey("order_item.id"),primary_key=True),
)