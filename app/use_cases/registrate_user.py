from datetime import datetime, timezone

from app.entities.user_entity import UserEntity
from app.exceptions.exceptions import UserAlreadyExistsError
from app.models.user_model import AuthResponse, UserCreate
from app.repositories.protocols.users_repository_protocol import UsersRepository
from app.services.token_service import TokenService
from app.utils.passlib_hash import hash_password


class RegisterUserUseCase:
    def __init__(
        self,
        user_repo: UsersRepository,
        token_service: TokenService,
    ):
        self._user_repo = user_repo
        self._token_service = token_service

    async def execute(self, user_data: UserCreate) -> AuthResponse:
        if await self._user_repo.exists_email(email=user_data.email):
            raise UserAlreadyExistsError("Пользователь с данным email уже существует")
        new_user = UserEntity(
            id=0,
            email=user_data.email,
            name=user_data.name,
            hashed_password=await hash_password(user_data.password),
            created_at=datetime.now(tz=timezone.utc),
        )
        user = await self._user_repo.create(new_user)
        access_token = self._token_service.create_access_token(user.id, user.email)
        return AuthResponse(access_token=access_token, token_type="Bearer")
