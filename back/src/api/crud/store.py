# from fastapi import APIRouter, Depends, HTTPException, Response
# from typing import List

# from src.models.user import Role
# from src.auth.index import required_role
# from src.errorHandler.index import ErrorHandler
# from src.db.engine import SessionDepend
# from src.models.store import *
# from src.crud.index import CRUD

# router = APIRouter(prefix="/store")

# @router.get(
#     "/",
#     response_model=List[ReadSchema],
#     dependencies=[Depends(required_role([Role.MANAGER]))],
# )
# def get_all(session: SessionDepend):
#     return CRUD.get_all(session, StoreModel)


# @router.post(
#     "/",
#     response_model=ReadSchema,
#     dependencies=[Depends(required_role([Role.CEO]))],
# )
# def create(create_data: CreateSchema, session: SessionDepend):
#     # same_name_item = (
#     #     session.query(StoreModel).filter(StoreModel.name == create_data.name).scalar()
#     # )
#     # if same_name_item:
#     #     return ErrorHandler.raise_409_same_name_item_exist()
#     return CRUD.create_one(session, StoreModel, create_data)


# @router.put(
#     "/{id}",
#     response_model=ReadSchema,
#     dependencies=[Depends(required_role([Role.CEO]))],
# )
# def update(update_data: UpdateSchema, session: SessionDepend, id: int):
#     # same_name_item = (
#     #     session.query(StoreModel)
#     #     .filter(StoreModel.name == update_data.name and StoreModel.id != id)
#     #     .first()
#     # )
#     # if same_name_item:
#     #     return ErrorHandler.raise_409_same_name_item_exist()
#     return CRUD.update_one_by_id(session, StoreModel, update_data, id)


# @router.delete(
#     "/{id}",
#     dependencies=[Depends(required_role([Role.CEO]))],
# )
# def delete(session: SessionDepend, id: int):
#     return CRUD.delete_one_by_id(session, StoreModel, id)
