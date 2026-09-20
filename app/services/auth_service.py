from app.models.user_model import AuthResponse, UserCreate, UserLogin
from app.repositories.protocols.users_repository_protocol import UsersRepository
from app.use_cases.login_user import LoginUserUseCase
from app.use_cases.registrate_user import RegisterUserUseCase


class AuthService:
    def __init__(
        self,
        user_repo: UsersRepository,
        register_uc: RegisterUserUseCase | None,
        login_uc: LoginUserUseCase | None,
    ):
        self._user_repo = user_repo
        self._register_uc = register_uc
        self._login_uc = login_uc

    async def register(self, new_user: UserCreate) -> AuthResponse | None:
        if self._register_uc:
            return await self._register_uc.execute(new_user)
        return None

    async def login(self, user: UserLogin) -> AuthResponse:
        return await self._login_uc.execute(user)
