from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config_settings import settings
from app.entities.user_entity import UserRole
from app.exceptions.exceptions import TokenError
from app.repositories.inmemory.inmemory_courses_repository import (
    InMemoryCourseRepository,
)
from app.repositories.inmemory.inmemory_lessons_repository import (
    InMemoryLessonRepository,
)
from app.repositories.inmemory.inmemory_users_repository import InMemoryUsersRepository
from app.repositories.protocols.users_repository_protocol import UsersRepository
from app.services.token_service import TokenService
from app.use_cases.change_user_role import ChangeUserRoleUseCase
from app.use_cases.create_course import CreateCourseUseCase
from app.use_cases.create_lesson import LessonCreateUseCase
from app.use_cases.get_course_lessons_list import GetCourseLessonsList
from app.use_cases.get_lesson_details import GetLessonDetailsUseCase
from app.use_cases.login_user import LoginUserUseCase
from app.use_cases.publish_course import PublishCourseUseCase
from app.use_cases.registrate_user import RegisterUserUseCase

bearer = HTTPBearer()
token_service = TokenService(settings.TOKEN_SECRET_KEY, settings.ALGORITHM)
users_repo = InMemoryUsersRepository()
courses_repo = InMemoryCourseRepository()
lessons_repo = InMemoryLessonRepository()


def get_inmemory_users_repo():
    return users_repo


def get_inmemory_courses_repo():
    return courses_repo


def get_inmemory_lessons_repo():
    return lessons_repo


def get_register_uc():
    return RegisterUserUseCase(users_repo, token_service)


def get_login_uc():
    return LoginUserUseCase(users_repo, token_service)


def get_create_course_uc():
    return CreateCourseUseCase(courses_repo, lessons_repo)


def get_change_user_role_uc():
    return ChangeUserRoleUseCase(users_repo)


def get_publish_course_uc():
    return PublishCourseUseCase(courses_repo)


def get_create_lesson_uc():
    return LessonCreateUseCase(lessons_repo, courses_repo)


def get_course_lessons_uc():
    return GetCourseLessonsList(courses_repo, lessons_repo)


def get_lesson_details_uc():
    return GetLessonDetailsUseCase(lessons_repo)


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
        user_repo: UsersRepository = Depends(get_inmemory_users_repo),
    ) -> int:
        user = await user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User Not Found")
        if user.role not in [role, UserRole.ADMIN]:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user_id

    return check
