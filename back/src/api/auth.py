from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta

from src.setting.index import get_settings
from src.auth.index import UserModel
from src.db.engine import SessionDepend
from src.errorHandler.index import ErrorHandler
from src.auth.index import (
    EXPIRE_STR_FORMAT,
    TokenResponse,
    create_access_token,
    TokenSourceData,
    get_user_model_by_email,
    check_user_password,
    get_current_user_by_token,
    get_routes_by_role_str,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login_to_get_access_token(
    session: SessionDepend, oauth2_form_data: OAuth2PasswordRequestForm = Depends()
):
    print(123)
    input_email, input_password = [oauth2_form_data.username, oauth2_form_data.password]
    user = get_user_model_by_email(session, input_email)
    if not user:
        return ErrorHandler.raise_401_unauthorized("錯誤的信箱或密碼")
    check_password = check_user_password(input_password, user.password)
    if not check_password:
        return ErrorHandler.raise_401_unauthorized("錯誤的信箱或密碼")
    setting = get_settings()
    expire_time = datetime.now() + timedelta(
        minutes=float(setting.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    str_expire_time = expire_time.strftime(EXPIRE_STR_FORMAT)
    access_token = create_access_token(
        TokenSourceData(user_email=input_email, str_expire_time=str_expire_time)
    )
    allow_route_name_list = get_routes_by_role_str(user.role_str)
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        allow_route_name_list=allow_route_name_list,
    )

@router.get("/check_token_when_first_enter")
def check_token_when_first_enter(user: UserModel = Depends(get_current_user_by_token)):
    allow_route_name_list = get_routes_by_role_str(user.role_str)
    return {"is_token_legal": True, "allow_route_name_list": allow_route_name_list}