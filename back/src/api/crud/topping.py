from fastapi import APIRouter, Depends, HTTPException, Response
from typing import List

from src.models.user import Role
from src.auth.index import required_role
from src.db.engine import SessionDepend
from src.crud.index import CRUD
from src.errorHandler.index import ErrorHandler
from src.models.topping import *

router = APIRouter(prefix="/topping",tags=["topping"])

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
    return CRUD.delete_one_by_id(session, ToppingModel, id)
