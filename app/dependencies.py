from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config_settings import settings
from app.entities.user_entity import UserRole
from app.exceptions.exceptions import TokenError
from app.repositories.inmemory.inmemory_courses_repository import (
    InMemoryCourseRepository,
)
from app.repositories.inmemory.inmemory_users_repository import InMemoryUsersRepository
from app.services.token_service import TokenService
from app.use_cases.create_course import CreateCourseUseCase
from app.use_cases.login_user import LoginUserUseCase
from app.use_cases.registrate_user import RegisterUserUseCase

bearer = HTTPBearer()
token_service = TokenService(settings.TOKEN_SECRET_KEY, settings.ALGORITHM)
users_repo = InMemoryUsersRepository()
courses_repo = InMemoryCourseRepository()


def get_inmemory_users_repo():
    return users_repo


def get_inmemory_courses_repo():
    return courses_repo


def get_register_uc():
    return RegisterUserUseCase(users_repo, token_service)


def get_login_uc():
    return LoginUserUseCase(users_repo, token_service)


def get_create_course_uc():
    return CreateCourseUseCase(courses_repo)


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
) -> int:
    token = credentials.credentials
    try:
        return token_service.verify_access_token(token)
    except TokenError as e:
        raise HTTPException(
            status_code=401, detail=str(e), headers={"WWW-Authenticate": "Bearer"}
        )


def require_role(role: UserRole):
    async def check(
        user_id: int = Depends(get_current_user_id),
        user_repo=Depends(get_inmemory_users_repo),
    ) -> int:
        user = await user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User Not Found")
        if user.role != role:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user_id

    return check
