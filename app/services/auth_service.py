from app.entities.user_entity import UserEntity
from app.models.user_model import UserCreate, UserLogin
from app.repositories.protocols.users_repository_protocol import UsersRepository
from app.use_cases.login_user import LoginUserUseCase
from app.use_cases.registrate_user import RegisterUserUseCase


class AuthService:
    def __init__(
        self,
        user_repo: UsersRepository,
        register_uc: RegisterUserUseCase,
        login_uc: LoginUserUseCase,
    ):
        self._user_repo = user_repo
        self._register_uc = register_uc
        self._login_uc = login_uc

    async def register(self, new_user: UserCreate) -> UserEntity:
        return await self._register_uc.execute(new_user)

    async def login(self, user: UserLogin) -> UserEntity:
        return await self._login_uc.execute(user)
