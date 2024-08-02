from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy import select

from src.auth.index import get_hashed_password
from src.db.engine import SessionDepend
from src.crud.index import CRUD
from src.models.user import *
from src.errorHandler.index import ErrorHandler
from src.auth.index import required_role
from src.utils.index import is_dev_environment

router = APIRouter(
    prefix="/user",
    dependencies=[Depends(required_role([Role.MANAGER]))],
    tags=["user"],
)


@router.get("/{id}", response_model=ReadSchema)
def get_one_by_id(session: SessionDepend, id: int):
    return CRUD.get_by_id(session, UserModel, id)


@router.get("/", response_model=List[ReadSchema])
def get_all(session: SessionDepend):
    return CRUD.get_all(session, UserModel)


@router.post("/", response_model=ReadSchema)
def create(create_data: CreateSchema, session: SessionDepend):
    same_email_user = (
        session.query(UserModel).filter(UserModel.email == create_data.email).first()
    )
    if same_email_user:
        return ErrorHandler.raise_409_same_name_item_exist("同信箱已存在")
    new_user = UserModel(email=create_data.email)
    new_user.role_str = create_data.role.value
    new_user.password = get_hashed_password(create_data.password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

@router.delete("/{id}")
def delete(session: SessionDepend, id: int):
    return CRUD.delete_one_by_id(session, UserModel, id)

class UpdatePassword(BaseModel):
    new_password: str
@router.put("/put_password/{id}", response_model=ReadSchema)
def update_password(update_data: UpdatePassword, session: SessionDepend, id: int):
    user = session.execute(select(UserModel).where(UserModel.id == id)).scalar()
    if not user:
        return ErrorHandler.raise_404_not_found("無此用戶")
    user.password = update_data.new_password
    session.commit()
    session.refresh(user)
    return user


class UpdateRole(BaseModel):
    new_role: Role
@router.put("/put_role/{id}", response_model=ReadSchema)
def update_role(update_data: UpdateRole, session: SessionDepend, id: int):
    user = session.execute(select(UserModel).where(UserModel.id == id)).scalar()
    if not user:
        return ErrorHandler.raise_404_not_found("無此用戶")
    user.role_str = update_data.new_role.value
    session.commit()
    session.refresh(user)
    return user

