from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from pydantic import BaseModel
from typing import TYPE_CHECKING
from sqlalchemy import Enum
import enum

from .base import BaseSQLModel, common_model_config_dict


@enum.unique
class Role(enum.Enum):
    CLERK = "CLERK"
    MANAGER = "MANAGER"
    ALL_ALLOW = "ALL_ALLOW"
    GUEST = "GUEST"


clerk_allow_route = ["create_order", "drink", "topping", "order"]
allow_route_name_map_by_role = {
    Role.CLERK: clerk_allow_route,
    Role.MANAGER: clerk_allow_route + ["user"],
    Role.GUEST: clerk_allow_route + ["user"],
}


class UserModel(BaseSQLModel):
    __tablename__ = "user"
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str]
    role_str: Mapped[str]  #TODO


class CreateSchema(BaseModel):
    email: str
    password: str
    role: Role


class UpdateRoleSchema(BaseModel):
    # password: str
    role: Role


class UpdatePasswordSchema(BaseModel):
    password: str


class ReadSchema(BaseModel):
    id: int
    email: str
    role_str: str
    model_config = common_model_config_dict
