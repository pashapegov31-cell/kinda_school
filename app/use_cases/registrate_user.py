from datetime import datetime, timezone

from app.entities.user_entity import UserEntity
from app.exceptions.exceptions import UserAlreadyExistsError
from app.models.user_model import UserCreate
from app.repositories.inmemory.inmemory_users_repository import InMemoryUsersRepository
from app.repositories.protocols.users_repository_protocol import UsersRepository

user_repo = InMemoryUsersRepository()


class RegisterUserUseCase:
    def __init__(self, user_repo: UsersRepository):
        self._user_repo = user_repo

    async def execute(self, user_data: UserCreate) -> UserEntity:
        if await user_repo.exists_email(email=user_data.email):
            raise UserAlreadyExistsError("Пользователь с данным email уже существует")
        new_user = UserEntity(
            id=0,
            email=user_data.email,
            name=user_data.name,
            hashed_password=user_data.password,
            created_at=datetime.now(tz=timezone.utc),
        )
        await self._user_repo.create(new_user)
        return new_user
