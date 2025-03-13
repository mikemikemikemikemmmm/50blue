from fastapi import APIRouter, Depends
from typing import List

from src.db.engine import SessionDepend
from src.models.drink import ReadSchema, DrinkModel, CreateSchema, UpdateSchema
from src.models.user import Role
from src.crud.index import CRUD
from src.auth.index import required_role

router = APIRouter(prefix="/drink",tags=["drink"])

# @router.get("/{id}", response_model=ReadSchema)
# def get_one_by_id(session: SessionDepend,id:int):
#     return CRUD.get_by_id(session,DrinkModel,id)


@router.get(
    "/",
    response_model=List[ReadSchema],
    dependencies=[Depends(required_role([Role.ALL_ALLOW]))],
)
def get_all(session: SessionDepend):
    return CRUD.get_all(session, DrinkModel)


@router.post(
    "/",
    response_model=ReadSchema,
    dependencies=[Depends(required_role([Role.MANAGER]))],
)
def create(create_data: CreateSchema, session: SessionDepend):
    return CRUD.create_one(session, DrinkModel, create_data)


@router.put(
    "/{id}",
    response_model=ReadSchema,
    dependencies=[Depends(required_role([Role.MANAGER]))],
)
def update(update_data: UpdateSchema, session: SessionDepend, id: int):
    return CRUD.update_one_by_id(session, DrinkModel, update_data, id)


@router.delete(
    "/{id}",
    dependencies=[Depends(required_role([Role.MANAGER]))],
)
def delete(session: SessionDepend, id: int):
    return CRUD.delete_one_by_id(session, DrinkModel, id)
