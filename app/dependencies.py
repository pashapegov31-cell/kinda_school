from app.core.config_settings import settings
from app.repositories.inmemory.inmemory_users_repository import InMemoryUsersRepository
from app.services.token_service import TokenService
from app.use_cases.login_user import LoginUserUseCase
from app.use_cases.registrate_user import RegisterUserUseCase

token_service = TokenService(settings.TOKEN_SECRET_KEY, settings.ALGORITHM)
users_repo = InMemoryUsersRepository()


def get_inmemory_user_repo():
    return users_repo


def get_register_uc():
    return RegisterUserUseCase(users_repo, token_service)


def get_login_uc():
    return LoginUserUseCase(users_repo, token_service)
