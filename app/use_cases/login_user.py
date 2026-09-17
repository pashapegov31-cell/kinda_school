from app.entities.user_entity import UserEntity
from app.exceptions.exceptions import LoginError
from app.models.user_model import UserLogin
from app.repositories.protocols.users_repository_protocol import UsersRepository
from app.utils.passlib_hash import verify_password


class LoginUserUseCase:
    def __init__(self, user_repo: UsersRepository):
        self._user_repo = user_repo

    async def execute(self, user: UserLogin) -> UserEntity:
        account = await self._user_repo.get_by_email(user.email)
        if not (
            account and await verify_password(user.password, account.hashed_password)
        ):
            raise LoginError("Введены некорректные данные")
        return account
