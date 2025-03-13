from fastapi import APIRouter, Depends
from typing import List

from src.models.user import Role
from src.auth.index import required_role
from src.db.engine import SessionDepend
from src.crud.index import CRUD
from src.errorHandler.index import ErrorHandler
from src.models.topping import *
from src.models.order_topping_table import order_item_toppings_table

router = APIRouter(prefix="/topping", tags=["topping"])


@router.get(
    "/",
    response_model=List[ReadSchema],
    dependencies=[Depends(required_role([Role.ALL_ALLOW]))],
)
def get_all(session: SessionDepend):
    return CRUD.get_all(session, ToppingModel)


@router.post(
    "/",
    response_model=ReadSchema,
    dependencies=[Depends(required_role([Role.MANAGER]))],
)
def create(create_data: CreateSchema, session: SessionDepend):
    return CRUD.create_one(session, ToppingModel, create_data)


@router.put(
    "/{id}",
    response_model=ReadSchema,
    dependencies=[Depends(required_role([Role.MANAGER]))],
)
def update(update_data: UpdateSchema, session: SessionDepend, id: int):
    return CRUD.update_one_by_id(session, ToppingModel, update_data, id)


@router.delete("/{id}", dependencies=[Depends(required_role([Role.MANAGER]))])
def delete(session: SessionDepend, id: int):
    be_ref_by_order_items = session.execute(
        order_item_toppings_table.select().where(
            order_item_toppings_table.c.topping_id == id
        )
    ).first()
    if be_ref_by_order_items:
        return ErrorHandler.raise_custom_error(code=400,detail="有訂單參考此配料")
    return CRUD.delete_one_by_id(session,ToppingModel,id)
    
