from app.models.user_model import UserCreate
from app.repositories.protocols.users_repository_protocol import UsersRepository
from app.use_cases.registrate_user import registrate_user


class AuthService:
    def __init__(self, session: UsersRepository):
        self.session = session

    @staticmethod
    async def register(session, user_data: UserCreate):
        await registrate_user(session, user_data)
