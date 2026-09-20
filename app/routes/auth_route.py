from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_login_uc, get_register_uc
from app.exceptions.exceptions import LoginError, UserAlreadyExistsError
from app.models.user_model import AuthResponse, UserCreate, UserLogin
from app.use_cases.login_user import LoginUserUseCase
from app.use_cases.registrate_user import RegisterUserUseCase

auth_router = APIRouter()


@auth_router.post("/register", response_model=AuthResponse)
async def register(
    user_data: UserCreate, register_uc: RegisterUserUseCase = Depends(get_register_uc)
):
    try:
        return await register_uc.execute(user_data)
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))


@auth_router.post("/login", response_model=AuthResponse)
async def login(
    user_data: UserLogin, login_uc: LoginUserUseCase = Depends(get_login_uc)
):
    try:
        return await login_uc.execute(user_data)
    except LoginError as e:
        raise HTTPException(status_code=400, detail=str(e))
