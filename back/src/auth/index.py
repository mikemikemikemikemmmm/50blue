from fastapi import Depends, status
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from typing import List
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime

from src.errorHandler.index import ErrorHandler
from src.models.user import UserModel, Role, allow_route_name_map_by_role
from src.db.engine import SessionDepend, Session
from src.setting.index import get_settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
setting = get_settings()

EXPIRE_STR_FORMAT = "%Y-%m-%d %H:%M:%S"

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    allow_route_name_list: list[str]


class TokenSourceData(BaseModel):
    user_email: str
    str_expire_time: str


pwd_context = CryptContext(schemes=["bcrypt"])


def get_hashed_password(password: str):
    return pwd_context.hash(password)


def get_user_by_email(session: Session, user_email: str) -> UserModel | None:
    return session.query(UserModel).filter(UserModel.email == user_email).first()


def create_access_token(token_source_data: TokenSourceData):
    data_copy = token_source_data.model_dump()
    encoded_jwt_token = jwt.encode(
        data_copy, setting.SECRET_KEY, algorithm=setting.ALGORITHM
    )
    return encoded_jwt_token


def get_current_user_by_token(
    session: SessionDepend, tokenStr: str = Depends(oauth2_scheme)
):
    try:
        payload = jwt.decode(
            tokenStr, setting.SECRET_KEY, algorithms=[setting.ALGORITHM]
        )
        token_data = TokenSourceData.model_validate(payload)
    except Exception as e:
        return ErrorHandler.raise_401_unauthorized("驗證錯誤")
    user = get_user_by_email(session, token_data.user_email)
    if user is None:
        return ErrorHandler.raise_401_unauthorized("驗證錯誤")
    expire_time = datetime.strptime(token_data.str_expire_time, EXPIRE_STR_FORMAT)
    if expire_time < datetime.now():
        return ErrorHandler.raise_401_unauthorized("驗證已過期")
    return user

def get_routes_by_role_str(role_str: str):
    try:
        role = get_role_from_string(role_str)
    except KeyError:
        return ErrorHandler.raise_403_no_permission()
    return allow_route_name_map_by_role.get(role, [])

def get_role_from_string(role_str):
    for role in Role:
        if role.value == role_str:
            return role
    return ErrorHandler.raise_500_server_error("角色錯誤")

def required_role(required_roles: List[Role]):
    def checker(user: UserModel = Depends(get_current_user_by_token)):
        role = get_role_from_string(user.role_str)
        if Role.ALL_ALLOW in required_roles or role in required_roles:
            return
        return ErrorHandler.raise_403_no_permission()
    return checker

def get_user_model_by_email(session: SessionDepend, input_email: str):
    return session.query(UserModel).filter(UserModel.email == input_email).first()

def check_user_password(input_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(input_password, hashed_password)
    except:
        return ErrorHandler.raise_500_server_error()
