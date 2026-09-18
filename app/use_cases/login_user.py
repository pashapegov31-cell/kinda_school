from app.exceptions.exceptions import LoginError, TokenError
from app.models.user_model import LoginResponse, UserLogin
from app.repositories.protocols.users_repository_protocol import UsersRepository
from app.services.token_service import TokenService
from app.utils.passlib_hash import verify_password


class LoginUserUseCase:
    def __init__(self, user_repo: UsersRepository, token_service: TokenService):
        self._user_repo = user_repo
        self._token_service = token_service

    async def execute(self, user: UserLogin) -> LoginResponse:
        account = await self._user_repo.get_by_email(user.email)
        if not (
            account and await verify_password(user.password, account.hashed_password)
        ):
            raise LoginError("Введены некорректные данные")
        access_token = self._token_service.create_access_token(
            account.id, account.email
        )
        if not access_token:
            raise TokenError("Токен не был создан")
        return LoginResponse(access_token=access_token, token_type="Bearer")
