from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy import text
import json

from src.crud.index import CRUD
from src.utils.index import get_all_drink
from src.errorHandler.index import ErrorHandler
from src.models.topping import ToppingModel
from src.db.engine import SessionDepend
from src.models.order import OrderModel, ReadSchema
from src.models.order_item import CreateSchema as OrderItemCreateSchema, OrderItemModel
from src.models.user import Role
from src.auth.index import required_role

router = APIRouter(prefix="/order",tags=["order"])


@router.delete(
    "/{id}", dependencies=[Depends(required_role([Role.MANAGER]))], response_model=int
)
def delete(session: SessionDepend, id: int):
    return CRUD.delete_one_by_id(session, OrderModel, id)


@router.get(
    "/",
    dependencies=[Depends(required_role([Role.ALL_ALLOW]))],
    response_model=List[ReadSchema],
)
def get_all(session: SessionDepend): 
    stmt = """
        SELECT 
            o.id AS id,
            o.created_at AS created_at,
            o.total_price AS total_price,
            (
                SELECT JSON_GROUP_ARRAY(
                    JSON_OBJECT(
                        'price', oi.price,
                        'ice_content', oi.ice_content,
                        'sugar_content', oi.sugar_content,
                        'drink_id', d.id,
                        'drink_name', d.name,
                        'topping_name_list', (
                            SELECT JSON_GROUP_ARRAY(
                                t.name
                            )
                            FROM topping t
                            JOIN order_item_toppings oit ON t.id = oit.topping_id
                            WHERE oit.order_item_id = oi.id
                        )
                    )
                )
                FROM order_item oi
                JOIN drink d ON oi.drink_id = d.id
                WHERE oi.order_id = o.id
            ) AS order_items
        FROM 'order' o
        ORDER BY o.created_at DESC
    """
    all_order = session.execute(text(stmt)).mappings().all()
    result = []
    for order in all_order:
        result.append(
            {
                "id": order["id"],
                "created_at": order["created_at"],
                "total_price": order["total_price"],
                "order_items": json.loads(order["order_items"]),
            }
        )
    return result


# for create


def get_target_drink(target_drink_id: int):
    all_drink = get_all_drink()
    for drink in all_drink:
        if drink.id == target_drink_id:
            return drink
    return ErrorHandler.raise_404_not_found(f"id:{target_drink_id} drink not found")


def create_order_item(create_data: OrderItemCreateSchema, session: SessionDepend):
    toppings = (
        session.query(ToppingModel)
        .filter(ToppingModel.id.in_(create_data.topping_ids))
        .all()
    )
    is_all_target_topping_exist = len(toppings) == len(create_data.topping_ids)
    if not is_all_target_topping_exist:
        return ErrorHandler.raise_404_not_found("some topping not found")
    drink = get_target_drink(create_data.drink_id)
    total_price = drink.price + sum(topping.price for topping in toppings)
    new_order_item = OrderItemModel(
        ice_content=create_data.ice_content,
        sugar_content=create_data.sugar_content,
        toppings=toppings,
        drink_id=create_data.drink_id,
        price=total_price,
    )
    session.add(new_order_item)
    session.commit()
    session.refresh(new_order_item)
    return new_order_item


@router.post(
    "/",
    dependencies=[Depends(required_role([Role.MANAGER, Role.CLERK]))],
)
def create_order(
    order_item_create_data_list: List[OrderItemCreateSchema], session: SessionDepend
):
    if len(order_item_create_data_list) == 0:
        return ErrorHandler.raise_404_not_found("order item not found")
    order_item_list = []
    total_price = 0
    for order_item_create_data in order_item_create_data_list:
        new_order_item = create_order_item(order_item_create_data, session)
        order_item_list.append(new_order_item)
        total_price += new_order_item.price
    new_order = OrderModel(order_items=order_item_list, total_price=total_price)
    session.add(new_order)
    session.commit()
    session.refresh(new_order)
    return new_order
