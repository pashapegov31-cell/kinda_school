from app.entities.user_entity import UserEntity
from app.models.user_model import UserCreate
from app.repositories.protocols.users_repository_protocol import UsersRepository
from app.use_cases.registrate_user import RegisterUserUseCase


class AuthService:
    def __init__(self, user_repo: UsersRepository, register_user: RegisterUserUseCase):
        self._register_user = register_user

    async def register_user(self, new_user: UserCreate) -> UserEntity:
        return await self._register_user.execute(new_user)
